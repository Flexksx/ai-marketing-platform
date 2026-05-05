import logging

from fastapi import APIRouter, BackgroundTasks, Depends, File, Form, Path, UploadFile
from supabase import AsyncClient

import src.content_generation_job.generation.runner as content_generation_runner
import src.content_generation_job.service as content_generation_job_service
from src.auth import get_async_supabase_service_client
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


router = APIRouter(tags=["Brand Content Generation Jobs"])

logger = logging.getLogger(__name__)


def _get_generate_fn(job: ContentGenerationJob):
    workflow_type = job.user_input.workflow_type
    if workflow_type == ContentGenerationJobWorkflowType.TEXT_WITH_SINGLE_IMAGE_FROM_USER_MEDIA:
        return generate_from_user_media_result
    if workflow_type == ContentGenerationJobWorkflowType.TEXT_WITH_SINGLE_IMAGE_AI_GENERATED:
        return generate_ai_image_result
    if workflow_type == ContentGenerationJobWorkflowType.TEXT_WITH_SINGLE_IMAGE_PRODUCT_LIFESTYLE:
        return generate_product_lifestyle_result
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
    supabase_client: AsyncClient = Depends(get_async_supabase_service_client),
):
    request_files = [request_file] if request_file else []
    request = await get_from_request_form(
        brand_id, request_data, request_files, supabase_client
    )

    job = await content_generation_job_service.create(request)
    generate = _get_generate_fn(job)

    logger.info(
        f"Dispatching content generation job {job.id}",
        extra={"job_id": job.id},
    )
    background_tasks.add_task(content_generation_runner.run, job.id, generate)

    return ContentGenerationJobResponse.model_validate(job)


@router.get("/{job_id}", response_model=ContentGenerationJobResponse)
async def get(
    brand_id: str = Depends(validate_brand_access),  # noqa: ARG001
    job_id: str = Path(...),
):
    job = await content_generation_job_service.get(job_id)
    return ContentGenerationJobResponse.model_validate(job)


@router.post("/{job_id}/accept", response_model=ContentResponse)
async def accept(
    job_id: str = Path(...),
    brand_id: str = Depends(validate_brand_access),  # noqa: ARG001
):
    job = await content_generation_job_service.accept(job_id)
    return ContentResponse.model_validate(job)
