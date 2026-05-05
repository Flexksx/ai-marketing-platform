import functools
import logging

from fastapi import APIRouter, BackgroundTasks, Depends, File, Form, Path, UploadFile

import src.content_generation_job.generation.runner as content_generation_runner
import src.content_generation_job.service as content_generation_job_service
from lib.db.session_factory import DbSessionFactory
from lib.supabase_client import SupabaseStorageService
from src.auth_access import validate_brand_access
from src.content.model import ContentResponse
from src.content_generation_job.errors import (
    ContentGenerationJobInvalidUserInputException,
)
from src.content_generation_job.factory import get_from_request_form
from src.content_generation_job.generation.text_with_single_image import (
    generate_ai_image_result,
    generate_from_user_media_result,
    generate_product_lifestyle_result,
)
from src.content_generation_job.model import (
    ContentGenerationJob,
    ContentGenerationJobResponse,
    ContentGenerationJobWorkflowType,
)
from src.shared.text_with_single_image import (
    TextWithSingleImageDeps,
    get_text_with_single_image_deps,
)


router = APIRouter(tags=["Brand Content Generation Jobs"])

logger = logging.getLogger(__name__)


def _get_generate_fn(
    job: ContentGenerationJob,
    session_factory: DbSessionFactory,
    content_deps: TextWithSingleImageDeps,
):
    workflow_type = job.user_input.workflow_type
    if (
        workflow_type
        == ContentGenerationJobWorkflowType.TEXT_WITH_SINGLE_IMAGE_FROM_USER_MEDIA
    ):
        return functools.partial(
            generate_from_user_media_result, session_factory=session_factory
        )
    if (
        workflow_type
        == ContentGenerationJobWorkflowType.TEXT_WITH_SINGLE_IMAGE_AI_GENERATED
    ):
        return functools.partial(generate_ai_image_result, content_deps=content_deps)
    if (
        workflow_type
        == ContentGenerationJobWorkflowType.TEXT_WITH_SINGLE_IMAGE_PRODUCT_LIFESTYLE
    ):
        return functools.partial(
            generate_product_lifestyle_result, content_deps=content_deps
        )
    raise ContentGenerationJobInvalidUserInputException(
        job.id,
        f"Workflow type {workflow_type} is not supported.",
    )


@router.post(
    "",
    response_model=ContentGenerationJobResponse,
    status_code=201,
)
async def start(
    background_tasks: BackgroundTasks,
    brand_id: str = Depends(validate_brand_access),
    request_data: str = Form(...),
    request_file: UploadFile | None = File(default=None),  # noqa: B008
    session_factory: DbSessionFactory = Depends(),
    supabase_storage_service: SupabaseStorageService = Depends(),
    content_deps: TextWithSingleImageDeps = Depends(get_text_with_single_image_deps),
):
    request_files = [request_file] if request_file else []
    request = await get_from_request_form(
        brand_id, request_data, request_files, supabase_storage_service
    )

    job = await content_generation_job_service.create(session_factory, request)
    generate = _get_generate_fn(job, session_factory, content_deps)

    logger.info(
        f"Dispatching content generation job {job.id}",
        extra={"job_id": job.id},
    )
    background_tasks.add_task(
        content_generation_runner.run, session_factory, job.id, generate
    )

    return ContentGenerationJobResponse.model_validate(job)


@router.get("/{job_id}", response_model=ContentGenerationJobResponse)
async def get(
    brand_id: str = Depends(validate_brand_access),  # noqa: ARG001
    job_id: str = Path(...),
    session_factory: DbSessionFactory = Depends(),
):
    job = await content_generation_job_service.get(session_factory, job_id)
    return ContentGenerationJobResponse.model_validate(job)


@router.post("/{job_id}/accept", response_model=ContentResponse)
async def accept(
    job_id: str = Path(...),
    brand_id: str = Depends(validate_brand_access),  # noqa: ARG001
    session_factory: DbSessionFactory = Depends(),
):
    job = await content_generation_job_service.accept(session_factory, job_id)
    return ContentResponse.model_validate(job)
