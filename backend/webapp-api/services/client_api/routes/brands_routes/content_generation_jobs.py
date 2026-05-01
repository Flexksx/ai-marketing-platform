import logging

from fastapi import APIRouter, Depends, File, Form, Path, UploadFile

from db.session_factory import DbSessionFactory
from services.client_api.auth.access_validation import validate_brand_access
from services.client_api.content_generation_job import get_from_request_form
from vozai.domain.content.schema import ContentResponse
from vozai.domain.content_generation_job import ContentGenerationJobResponse
import vozai.domain.content_generation_job.service as content_generation_job_service
from vozai.lib.cloudtasks.service import CloudTasksService
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
    session_factory: DbSessionFactory = Depends(),
    tasks_service: CloudTasksService = Depends(),
    supabase_storage_service: SupabaseStorageService = Depends(),
):
    request_files = [request_file] if request_file else []
    request = await get_from_request_form(
        brand_id, request_data, request_files, supabase_storage_service
    )

    job = await content_generation_job_service.start(
        session_factory,
        tasks_service,
        request,
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
