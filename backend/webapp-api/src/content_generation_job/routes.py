import logging

from fastapi import APIRouter, BackgroundTasks, Depends, File, Form, Path, UploadFile

import src.content_generation_job.service as content_generation_job_service
from lib.db.session_factory import DbSessionFactory
from src.auth_access import validate_brand_access
from webapp_api_contract.content import ContentResponse
from webapp_api_contract.content_generation import ContentGenerationJobResponse
from src.content_generation_job.factory import get_from_request_form
from src.content_generation_job.generation.factory import (
    ContentGenerationJobRunnerFactory,
)
from lib.supabase_client import (
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
    background_tasks: BackgroundTasks,
    brand_id: str = Depends(validate_brand_access),
    request_data: str = Form(...),
    request_file: UploadFile | None = File(default=None),  # noqa: B008
    session_factory: DbSessionFactory = Depends(),
    factory: ContentGenerationJobRunnerFactory = Depends(),
    supabase_storage_service: SupabaseStorageService = Depends(),
):
    request_files = [request_file] if request_file else []
    request = await get_from_request_form(
        brand_id, request_data, request_files, supabase_storage_service
    )

    job = await content_generation_job_service.create(session_factory, request)
    runner = factory.get_runner(job)

    logger.info(
        f"Dispatching content generation job {job.id} with runner {type(runner).__name__}",
        extra={"job_id": job.id},
    )
    background_tasks.add_task(runner.process, job.id)

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
