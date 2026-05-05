import functools
import logging

from fastapi import (
    APIRouter,
    BackgroundTasks,
    Body,
    Depends,
    File,
    Form,
    Path,
    UploadFile,
)

import src.campaign_generation.service as campaign_generation_job_service
from lib.db.session_factory import DbSessionFactory
from lib.prompts import PromptTemplateName
from lib.supabase_client import SupabaseStorageService
from src.auth import get_current_user_id
from src.auth_access import validate_brand_access
from src.campaign_generation.errors import (
    CampaignGenerationJobWorkflowTypeMismatchException,
)
from src.campaign_generation.factory import get_from_request_form
from src.campaign_generation.generation.content_brief import (
    ai_generated as ai_generated_brief,
)
from src.campaign_generation.generation.content_brief import (
    from_user_media as user_media_brief,
)
from src.campaign_generation.generation.content_generation import (
    ai_generated as ai_generated_content,
)
from src.campaign_generation.generation.content_generation import (
    from_user_media as user_media_content,
)
from src.campaign_generation.generation.content_generation import (
    product_lifestyle as product_lifestyle_content,
)
from src.campaign_generation.generation.content_plan import (
    ai_generated as ai_generated_plan,
)
from src.campaign_generation.generation.content_plan import (
    from_user_media as user_media_plan,
)
from src.campaign_generation.generation.shared.service import (
    run_campaign_generation_job,
)
from src.campaign_generation.model import (
    CampaignCreationAcceptRequest,
    CampaignGenerationJob,
    CampaignGenerationJobResponse,
    CampaignGenerationJobWorkflowType,
)
from src.campaigns.model import CampaignResponse
from src.shared import TextWithSingleImageContentGenerator


router = APIRouter(tags=["Brand Campaign Creation"])

logger = logging.getLogger(__name__)


def _get_campaign_steps(
    job: CampaignGenerationJob,
    session_factory: DbSessionFactory,
    content_generator: TextWithSingleImageContentGenerator,
) -> tuple:
    workflow_type = job.workflow_type

    if workflow_type == CampaignGenerationJobWorkflowType.AI_GENERATED:
        return (
            functools.partial(
                ai_generated_brief.generate_content_brief,
                session_factory=session_factory,
            ),
            functools.partial(
                ai_generated_plan.generate_content_plan,
                session_factory=session_factory,
                prompt_template_name=PromptTemplateName.CAMPAIGN_GENERATION_CONTENT_PLAN_STEP,
            ),
            functools.partial(
                ai_generated_content.generate_content,
                session_factory=session_factory,
                content_generator=content_generator,
            ),
        )
    if workflow_type == CampaignGenerationJobWorkflowType.USER_MEDIA_ONLY:
        return (
            functools.partial(
                user_media_brief.generate_content_brief, session_factory=session_factory
            ),
            functools.partial(
                user_media_plan.generate_content_plan, session_factory=session_factory
            ),
            functools.partial(
                user_media_content.generate_content,
                session_factory=session_factory,
                content_generator=content_generator,
            ),
        )
    if workflow_type == CampaignGenerationJobWorkflowType.PRODUCT_LIFESTYLE:
        return (
            functools.partial(
                ai_generated_brief.generate_content_brief,
                session_factory=session_factory,
            ),
            functools.partial(
                ai_generated_plan.generate_content_plan,
                session_factory=session_factory,
                prompt_template_name=PromptTemplateName.CAMPAIGN_GENERATION_CONTENT_PLAN_STEP,
            ),
            functools.partial(
                product_lifestyle_content.generate_content,
                session_factory=session_factory,
                content_generator=content_generator,
            ),
        )
    raise CampaignGenerationJobWorkflowTypeMismatchException(
        f"No steps defined for workflow type: {workflow_type}"
    )


@router.post(
    "",
    response_model=CampaignGenerationJobResponse,
    status_code=201,
)
async def start(
    background_tasks: BackgroundTasks,
    user_id: str = Depends(get_current_user_id),  # noqa: ARG001
    brand_id: str = Depends(validate_brand_access),
    request_data: str = Form(...),
    request_files: list[UploadFile] = File(default=[]),  # noqa: B008
    session_factory: DbSessionFactory = Depends(),
    supabase_storage_service: SupabaseStorageService = Depends(),
    content_generator: TextWithSingleImageContentGenerator = Depends(),
):
    request = await get_from_request_form(
        brand_id, request_data, request_files, supabase_storage_service
    )

    job = await campaign_generation_job_service.create(session_factory, request)
    brief_fn, plan_fn, content_fn = _get_campaign_steps(
        job, session_factory, content_generator
    )

    logger.info(
        f"Dispatching campaign generation job {job.id} for workflow {job.workflow_type}",
        extra={"job_id": job.id},
    )
    background_tasks.add_task(
        run_campaign_generation_job,
        session_factory,
        job.id,
        brief_fn,
        plan_fn,
        content_fn,
    )

    return CampaignGenerationJobResponse.model_validate(job)


@router.get("/{job_id}", response_model=CampaignGenerationJobResponse)
async def get(
    job_id: str = Path(...),
    brand_id: str = Depends(validate_brand_access),  # noqa: ARG001
    session_factory: DbSessionFactory = Depends(),
):
    job = await campaign_generation_job_service.get(session_factory, job_id)
    return CampaignGenerationJobResponse.model_validate(job)


@router.post("/{job_id}/accept", response_model=CampaignResponse)
async def accept(
    job_id: str = Path(...),
    request: CampaignCreationAcceptRequest = Body(...),  # noqa: B008
    brand_id: str = Depends(validate_brand_access),  # noqa: ARG001
    session_factory: DbSessionFactory = Depends(),
):
    campaign = await campaign_generation_job_service.accept(
        session_factory,
        job_id,
        request,
    )
    return CampaignResponse.model_validate(campaign)
