import public
from fastapi import Depends, Path

import vozai.domain.brand.service as brand_service
import vozai.domain.brand_extraction.service as brand_generation_job_service
import vozai.domain.campaign_generation.service as campaign_generation_job_service
from db.session_factory import DbSessionFactory
from vozai.auth import get_current_user_id
from vozai.domain.brand import BrandNotFoundError
from vozai.domain.brand_extraction import BrandGenerationJobNotFoundError
from vozai.domain.campaign_generation.errors import (
    CampaignGenerationJobNotFoundException,
)


@public.add
async def validate_brand_access(
    brand_id: str = Path(...),
    user_id: str = Depends(get_current_user_id),
    session_factory: DbSessionFactory = Depends(),
) -> str:
    has_access = await brand_service.validate_access(
        session_factory,
        brand_id,
        user_id,
    )
    if not has_access:
        raise BrandNotFoundError(brand_id)
    return brand_id


@public.add
async def validate_campaign_generation_job_access(
    job_id: str = Path(...),
    user_id: str = Depends(get_current_user_id),
    session_factory: DbSessionFactory = Depends(),
) -> str:
    has_access = await campaign_generation_job_service.validate_access(
        session_factory, job_id, user_id
    )
    if not has_access:
        raise CampaignGenerationJobNotFoundException(job_id)
    return job_id


@public.add
async def validate_brand_generation_job_access(
    job_id: str = Path(...),
    user_id: str = Depends(get_current_user_id),
    session_factory: DbSessionFactory = Depends(),
) -> str:
    has_access = await brand_generation_job_service.validate_access(
        session_factory, job_id, user_id
    )
    if not has_access:
        raise BrandGenerationJobNotFoundError(job_id)
    return job_id
