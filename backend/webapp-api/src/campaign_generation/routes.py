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

import src.campaign_generation.generation.runner as campaign_generation_runner
import src.campaign_generation.service as campaign_generation_job_service
from lib.db.session_factory import DbSessionFactory
from lib.supabase_client import SupabaseStorageService
from src.auth import get_current_user_id
from src.auth_access import validate_brand_access
from src.campaign_generation.factory import get_from_request_form
from src.campaign_generation.model import (
    CampaignCreationAcceptRequest,
    CampaignGenerationJobResponse,
)
from src.campaigns.model import CampaignResponse
from src.shared.text_with_single_image import TextWithSingleImageContentGenerator


router = APIRouter(tags=["Brand Campaign Creation"])

logger = logging.getLogger(__name__)


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

    logger.info(
        f"Dispatching campaign generation job {job.id} "
        f"for workflow {job.workflow_type}",
        extra={"job_id": job.id},
    )
    background_tasks.add_task(
        campaign_generation_runner.run, job, session_factory, content_generator
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
