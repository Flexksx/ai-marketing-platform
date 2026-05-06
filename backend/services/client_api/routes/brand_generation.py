import logging

from fastapi import APIRouter, Body, Depends

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
    BrandGenerationJobService,
)


router = APIRouter(prefix="/brand-generation", tags=["brand-generation"])

logger = logging.getLogger(__name__)


@router.post("", response_model=BrandGenerationJob, status_code=201)
async def start(
    user_id: str = Depends(get_current_user_id),
    request: BrandGenerationJobCreateRequestBody = Body(...),  # noqa: B008
    brand_generation_job_service: BrandGenerationJobService = Depends(),
):
    create_request = BrandGenerationJobCreateRequest(
        website_url=request.website_url,
    )
    return await brand_generation_job_service.start(user_id, create_request)


@router.get("/{job_id}", response_model=BrandGenerationJobResponse)
async def get(
    job_id: str = Depends(validate_brand_generation_job_access),
    service: BrandGenerationJobService = Depends(),
):
    return await service.get(job_id)


@router.post("/{job_id}/accept", response_model=BrandResponse)
async def accept(
    job_id: str = Depends(validate_brand_generation_job_access),
    request: BrandGenerationJobAcceptRequest = Body(...),  # noqa: B008
    service: BrandGenerationJobService = Depends(),
):
    return await service.accept(job_id, request)
