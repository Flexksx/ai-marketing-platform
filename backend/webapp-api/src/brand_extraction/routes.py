import logging

from fastapi import APIRouter, Body, Depends, Header, HTTPException, status

import src.brand_extraction.service as brand_generation_job_service
from lib.db.session_factory import DbSessionFactory
from src.auth import get_current_user_id
from src.auth_access import validate_brand_generation_job_access
from src.config import get_settings
from webapp_api_contract.brands import BrandResponse
from webapp_api_contract.brand_extraction import (
    BrandGenerationJob,
    BrandGenerationJobAcceptRequest,
    BrandGenerationJobCreateRequest,
    BrandGenerationJobCreateRequestBody,
    BrandGenerationJobResponse,
)
from scraper_api_contract.scraper import ScrapeResult


router = APIRouter(prefix="/brand-generation", tags=["brand-generation"])

logger = logging.getLogger(__name__)


@router.post("", response_model=BrandGenerationJob, status_code=201)
async def start(
    user_id: str = Depends(get_current_user_id),
    request: BrandGenerationJobCreateRequestBody = Body(...),  # noqa: B008
    session_factory: DbSessionFactory = Depends(),
):
    create_request = BrandGenerationJobCreateRequest(
        website_url=request.website_url,
    )
    return await brand_generation_job_service.start(
        session_factory,
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


@router.put("/{job_id}/scrape-result", status_code=202)
async def receive_scrape_result(
    job_id: str,
    scrape_result: ScrapeResult = Body(...),  # noqa: B008
    session_factory: DbSessionFactory = Depends(),
    x_callback_secret: str | None = Header(default=None),
):
    settings = get_settings()
    if x_callback_secret != settings.scraper_callback_secret:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid callback secret",
        )

    logger.info(
        f"Received scrape result for brand generation job {job_id}",
        extra={"job_id": job_id},
    )

    await brand_generation_job_service.resume_after_scrape(
        session_factory, job_id, scrape_result
    )

    return {"status": "accepted", "job_id": job_id}
