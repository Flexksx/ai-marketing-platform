import public
from fastapi import Depends, Path

import src.brand.service as brand_service
import src.brand_generation_job.service as brand_generation_job_service
import src.campaign_generation.service as campaign_generation_job_service
from src.auth import get_current_user_id
from src.brand.errors import BrandNotFoundError
from src.brand_generation_job.errors import BrandGenerationJobNotFoundError
from src.campaign_generation.errors import (
    CampaignGenerationJobNotFoundException,
)


@public.add
async def validate_brand_access(
    brand_id: str = Path(...),
    user_id: str = Depends(get_current_user_id),
) -> str:
    has_access = await brand_service.validate_access(brand_id, user_id)
    if not has_access:
        raise BrandNotFoundError(brand_id)
    return brand_id


@public.add
async def validate_campaign_generation_job_access(
    job_id: str = Path(...),
    user_id: str = Depends(get_current_user_id),
) -> str:
    has_access = await campaign_generation_job_service.validate_access(job_id, user_id)
    if not has_access:
        raise CampaignGenerationJobNotFoundException(job_id)
    return job_id


@public.add
async def validate_brand_generation_job_access(
    job_id: str = Path(...),
    user_id: str = Depends(get_current_user_id),
) -> str:
    has_access = await brand_generation_job_service.validate_access(job_id, user_id)
    if not has_access:
        raise BrandGenerationJobNotFoundError(job_id)
    return job_id
