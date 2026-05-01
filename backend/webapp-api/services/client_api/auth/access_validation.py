import public
from fastapi import Depends, Path

from vozai.auth import get_current_user_id
from vozai.domain.brand import BrandNotFoundError, BrandService
from vozai.domain.brand_extraction import (
    BrandGenerationJobNotFoundError,
    BrandGenerationJobService,
)
from vozai.domain.campaign_generation import (
    CampaignGenerationJobService,
)
from vozai.domain.campaign_generation.errors import (
    CampaignGenerationJobNotFoundException,
)


@public.add
async def validate_brand_access(
    brand_id: str = Path(...),
    user_id: str = Depends(get_current_user_id),
    brand_service: BrandService = Depends(),
) -> str:
    has_access = await brand_service.validate_access(brand_id, user_id)
    if not has_access:
        raise BrandNotFoundError(brand_id)
    return brand_id


@public.add
async def validate_campaign_generation_job_access(
    job_id: str = Path(...),
    user_id: str = Depends(get_current_user_id),
    campaign_generation_job_service: CampaignGenerationJobService = Depends(),
) -> str:
    has_access = await campaign_generation_job_service.validate_access(job_id, user_id)
    if not has_access:
        raise CampaignGenerationJobNotFoundException(job_id)
    return job_id


@public.add
async def validate_brand_generation_job_access(
    job_id: str = Path(...),
    user_id: str = Depends(get_current_user_id),
    brand_generation_job_service: BrandGenerationJobService = Depends(),
) -> str:
    has_access = await brand_generation_job_service.validate_access(job_id, user_id)
    if not has_access:
        raise BrandGenerationJobNotFoundError(job_id)
    return job_id
