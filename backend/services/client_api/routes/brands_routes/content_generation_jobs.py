import logging

from fastapi import APIRouter, Depends, File, Form, Path, UploadFile

from services.client_api.auth.access_validation import validate_brand_access
from services.client_api.content_generation_job import get_from_request_form
from vozai.domain.content.schema import ContentResponse
from vozai.domain.content_generation_job import (
    ContentGenerationJobResponse,
    ContentGenerationJobService,
)
from vozai.lib.supabase_client import (
    SupabaseStorageService,
)


router = APIRouter(tags=["Brand Content Generation Jobs"])


logger = logging.getLogger(__name__)


@router.post(
    "",
    response_model=ContentGenerationJobResponse,
    status_code=201,
)
async def start(
    brand_id: str = Depends(validate_brand_access),
    request_data: str = Form(...),
    request_file: UploadFile | None = File(default=None),  # noqa: B008
    content_generation_job_service: ContentGenerationJobService = Depends(),
    supabase_storage_service: SupabaseStorageService = Depends(),
):
    request_files = [request_file] if request_file else []
    request = await get_from_request_form(
        brand_id, request_data, request_files, supabase_storage_service
    )

    job = await content_generation_job_service.start(request)

    return ContentGenerationJobResponse.model_validate(job)


@router.get("/{job_id}", response_model=ContentGenerationJobResponse)
async def get(
    brand_id: str = Depends(validate_brand_access),  # noqa: ARG001
    job_id: str = Path(...),
    content_generation_job_service: ContentGenerationJobService = Depends(),
):
    job = await content_generation_job_service.get(job_id)
    return ContentGenerationJobResponse.model_validate(job)


@router.post("/{job_id}/accept", response_model=ContentResponse)
async def accept(
    job_id: str = Path(...),
    brand_id: str = Depends(validate_brand_access),  # noqa: ARG001
    content_generation_job_service: ContentGenerationJobService = Depends(),
):
    job = await content_generation_job_service.accept(job_id)
    return ContentResponse.model_validate(job)
