import logging

from fastapi import APIRouter, BackgroundTasks, Body, Depends

import src.brand_generation_job.service as brand_generation_job_service
from lib.db.session_factory import DbSessionFactory
from lib.scraper.dependencies import get_playwright_scraper
from lib.scraper.playwright_scraper import PlaywrightScraper
from src.auth import get_current_user_id
from src.auth_access import validate_brand_generation_job_access
from src.brand.model import BrandResponse
from src.brand_generation_job.model import (
    BrandGenerationJob,
    BrandGenerationJobAcceptRequest,
    BrandGenerationJobCreateRequest,
    BrandGenerationJobCreateRequestBody,
    BrandGenerationJobResponse,
)


router = APIRouter(prefix="/brand-generation", tags=["brand-generation"])

logger = logging.getLogger(__name__)


@router.post("", response_model=BrandGenerationJob, status_code=201)
async def start(
    background_tasks: BackgroundTasks,
    user_id: str = Depends(get_current_user_id),
    request: BrandGenerationJobCreateRequestBody = Body(...),  # noqa: B008
    session_factory: DbSessionFactory = Depends(),
    scraper: PlaywrightScraper = Depends(get_playwright_scraper),
):
    create_request = BrandGenerationJobCreateRequest(
        website_url=request.website_url,
    )
    return await brand_generation_job_service.start(
        session_factory,
        user_id,
        create_request,
        scraper,
        background_tasks,
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
