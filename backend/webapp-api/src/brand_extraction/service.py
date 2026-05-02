import asyncio
import logging

import httpx
from scraper_api_contract.scraper import ScrapeResult

import src.brand_extraction.repository as brand_generation_job_repository
import src.brands.service as brand_service
from lib.db.session_factory import DbSessionFactory
from lib.prompts.service import PromptService
from src.brand_extraction.generation.steps.data_extraction import (
    BrandDataExtractionStep,
)
from src.config import get_settings
from webapp_api_contract.brand_extraction import (
    BrandGenerationJob,
    BrandGenerationJobAcceptRequest,
    BrandGenerationJobCreateRequest,
    BrandGenerationJobUpdateRequest,
    BrandGenerationResult,
)
from webapp_api_contract.brands import Brand, BrandCreateRequest
from webapp_api_contract.shared import JobStatus


logger = logging.getLogger(__name__)

SCRAPER_CALLBACK_SECRET_HEADER = "X-Callback-Secret"

_background_tasks: set[asyncio.Task] = set()


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
) -> BrandGenerationJob:
    job = await create(session_factory, user_id, request)
    task = asyncio.create_task(_dispatch_scrape_request(job.id, job.website_url))
    _background_tasks.add(task)
    task.add_done_callback(_background_tasks.discard)
    return job


async def resume_after_scrape(
    session_factory: DbSessionFactory,
    job_id: str,
    scrape_result: ScrapeResult,
) -> None:
    job = await update(
        session_factory,
        job_id,
        BrandGenerationJobUpdateRequest(
            status=JobStatus.IN_PROGRESS,
            result=BrandGenerationResult(scraper_result=scrape_result, brand_data=None),
        ),
    )

    prompt_service = PromptService()
    extraction_step = BrandDataExtractionStep(prompt_service=prompt_service)

    task = asyncio.create_task(
        _run_data_extraction(session_factory, job, extraction_step)
    )
    _background_tasks.add(task)
    task.add_done_callback(_background_tasks.discard)


async def _run_data_extraction(
    session_factory: DbSessionFactory,
    job: BrandGenerationJob,
    extraction_step,
) -> None:
    try:
        result = await extraction_step.execute(job)
        await update(
            session_factory,
            job.id,
            BrandGenerationJobUpdateRequest(
                status=JobStatus.COMPLETED,
                result=result,
            ),
        )
        logger.info(
            f"Brand generation job {job.id} completed", extra={"job_id": job.id}
        )
    except Exception as exception:
        logger.error(
            f"Brand generation job {job.id} failed during data extraction: {exception}",
            exc_info=True,
            extra={"job_id": job.id},
        )
        await _mark_job_failed(session_factory, job.id)


async def _mark_job_failed(
    session_factory: DbSessionFactory,
    job_id: str,
) -> None:
    try:
        existing = await get(session_factory, job_id)
        scrape_result = existing.result.scraper_result if existing.result else None
        await update(
            session_factory,
            job_id,
            BrandGenerationJobUpdateRequest(
                status=JobStatus.FAILED,
                result=BrandGenerationResult(
                    scraper_result=scrape_result, brand_data=None
                ),
            ),
        )
    except Exception as update_error:
        logger.error(
            f"Failed to mark job {job_id} as failed: {update_error}",
            extra={"job_id": job_id},
        )


async def _dispatch_scrape_request(job_id: str, website_url: str) -> None:
    settings = get_settings()
    callback_url = (
        f"{settings.api_base_url.rstrip('/')}/brand-generation/{job_id}/scrape-result"
    )
    scraper_url = f"{settings.scraper_service_url.rstrip('/')}/scrape"

    logger.info(
        f"Dispatching scrape request for job {job_id} to {scraper_url}",
        extra={"job_id": job_id},
    )

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(
                scraper_url,
                json={
                    "url": website_url,
                    "callback_url": callback_url,
                    "callback_secret": settings.scraper_callback_secret,
                },
            )
            response.raise_for_status()
            logger.info(
                f"Scrape request accepted for job {job_id}",
                extra={"job_id": job_id},
            )
    except Exception as error:
        logger.error(
            f"Failed to dispatch scrape request for job {job_id}: {error}",
            exc_info=True,
            extra={"job_id": job_id},
        )


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
