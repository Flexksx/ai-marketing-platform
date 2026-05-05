import logging

from fastapi import BackgroundTasks

import src.brand.service as brand_service
import src.brand_generation_job.repository as brand_generation_job_repository
from lib.db.session_factory import DbSessionFactory
from lib.scraper.playwright_scraper import PlaywrightScraper
from src.brand.model import Brand, BrandCreateRequest
from src.brand_generation_job.generation.service import run_brand_generation_job
from src.brand_generation_job.model import (
    BrandGenerationJob,
    BrandGenerationJobAcceptRequest,
    BrandGenerationJobCreateRequest,
    BrandGenerationJobUpdateRequest,
)


logger = logging.getLogger(__name__)


async def create(
    session_factory: DbSessionFactory,
    user_id: str,
    request: BrandGenerationJobCreateRequest,
) -> BrandGenerationJob:
    return await brand_generation_job_repository.create(
        session_factory,
        user_id,
        request,
    )


async def get(
    session_factory: DbSessionFactory,
    job_id: str,
) -> BrandGenerationJob:
    return await brand_generation_job_repository.get(session_factory, job_id)


async def update(
    session_factory: DbSessionFactory,
    job_id: str,
    request: BrandGenerationJobUpdateRequest,
) -> BrandGenerationJob:
    return await brand_generation_job_repository.update(
        session_factory,
        job_id,
        request,
    )


async def start(
    session_factory: DbSessionFactory,
    user_id: str,
    request: BrandGenerationJobCreateRequest,
    scraper: PlaywrightScraper,
    background_tasks: BackgroundTasks,
) -> BrandGenerationJob:
    job = await create(session_factory, user_id, request)
    background_tasks.add_task(
        run_brand_generation_job, session_factory, scraper, job.id
    )
    return job


async def accept(
    session_factory: DbSessionFactory,
    job_id: str,
    request: BrandGenerationJobAcceptRequest,
) -> Brand:
    job = await get(session_factory, job_id)
    brand_input = BrandCreateRequest(name=request.name, data=request.data)
    return await brand_service.create(
        session_factory,
        job.user_id,
        brand_input,
    )


async def validate_access(
    session_factory: DbSessionFactory,
    job_id: str,
    user_id: str,
) -> bool:
    return await brand_generation_job_repository.exists_for_user(
        session_factory,
        job_id,
        user_id,
    )
