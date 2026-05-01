import logging

from fastapi import APIRouter, Body, Depends

import vozai.domain.brand_extraction.service as brand_generation_job_service
from db.session_factory import DbSessionFactory
from services.client_api.auth.access_validation import (
    validate_brand_generation_job_access,
)
from vozai.auth import get_current_user_id
from vozai.domain.brand.schema import BrandResponse
from vozai.domain.brand_extraction import (
    BrandGenerationJob,
    BrandGenerationJobAcceptRequest,
    BrandGenerationJobCreateRequest,
    BrandGenerationJobCreateRequestBody,
    BrandGenerationJobResponse,
)
from vozai.lib.cloudtasks.service import CloudTasksService


router = APIRouter(prefix="/brand-generation", tags=["brand-generation"])

logger = logging.getLogger(__name__)


@router.post("", response_model=BrandGenerationJob, status_code=201)
async def start(
    user_id: str = Depends(get_current_user_id),
    request: BrandGenerationJobCreateRequestBody = Body(...),  # noqa: B008
    session_factory: DbSessionFactory = Depends(),
    tasks_service: CloudTasksService = Depends(),
):
    create_request = BrandGenerationJobCreateRequest(
        website_url=request.website_url,
    )
    return await brand_generation_job_service.start(
        session_factory,
        tasks_service,
        user_id,
        create_request,
    )


@router.get("/{job_id}", response_model=BrandGenerationJobResponse)
async def get(
    job_id: str = Depends(validate_brand_generation_job_access),
    session_factory: DbSessionFactory = Depends(),
):
    return await brand_generation_job_service.get(session_factory, job_id)


@router.post("/{job_id}/accept", response_model=BrandResponse)
async def accept(
    job_id: str = Depends(validate_brand_generation_job_access),
    request: BrandGenerationJobAcceptRequest = Body(...),  # noqa: B008
    session_factory: DbSessionFactory = Depends(),
):
    return await brand_generation_job_service.accept(session_factory, job_id, request)
