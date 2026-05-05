import logging

import src.brand_generation_job.service as brand_generation_job_service
from lib.db.session_factory import DbSessionFactory
from lib.scraper.playwright_scraper import PlaywrightScraper
from src.brand_generation_job.generation.steps.data_extraction import extract_brand_data
from src.brand_generation_job.generation.steps.scraping import scrape_brand
from src.brand_generation_job.model import (
    BrandGenerationJob,
    BrandGenerationJobUpdateRequest,
    BrandGenerationResult,
)
from src.shared.model import JobStatus


logger = logging.getLogger(__name__)


async def run_brand_generation_job(
    session_factory: DbSessionFactory,
    scraper: PlaywrightScraper,
    job_id: str,
) -> BrandGenerationJob:
    try:
        job = await brand_generation_job_service.get(session_factory, job_id)

        if job.result:
            await _update_job(
                session_factory, job_id, JobStatus.IN_PROGRESS, job.result
            )
        logger.info(
            f"Job {job_id} status updated to IN_PROGRESS",
            extra={"job_id": job_id},
        )

        logger.info(
            f"Processing scraping step for job {job_id}",
            extra={"job_id": job_id},
        )
        scraping_result = await scrape_brand(scraper, job)
        job = await _update_job(
            session_factory, job_id, JobStatus.IN_PROGRESS, scraping_result
        )
        logger.info(
            f"Scraping step completed for job {job_id}",
            extra={"job_id": job_id},
        )

        logger.info(
            f"Processing data extraction step for job {job_id}",
            extra={"job_id": job_id},
        )
        data_extraction_result = await extract_brand_data(job)
        job = await _update_job(
            session_factory, job_id, JobStatus.COMPLETED, data_extraction_result
        )
        logger.info(
            f"Data extraction step completed for job {job_id}",
            extra={"job_id": job_id},
        )

        logger.info(
            f"Job {job_id} completed with status {job.status}",
            extra={"job_id": job_id},
        )
        return job

    except Exception as exception:
        logger.error(
            f"Job {job_id} failed: {exception}",
            exc_info=True,
            extra={"job_id": job_id},
        )
        await _mark_job_failed(session_factory, job_id)
        raise


async def _update_job(
    session_factory: DbSessionFactory,
    job_id: str,
    status: JobStatus,
    result: BrandGenerationResult,
) -> BrandGenerationJob:
    return await brand_generation_job_service.update(
        session_factory,
        job_id,
        BrandGenerationJobUpdateRequest(status=status, result=result),
    )


async def _mark_job_failed(
    session_factory: DbSessionFactory,
    job_id: str,
) -> None:
    job = await brand_generation_job_service.get(session_factory, job_id)
    scrape_result = job.result.scraper_result if job.result else None
    await brand_generation_job_service.update(
        session_factory,
        job_id,
        BrandGenerationJobUpdateRequest(
            status=JobStatus.FAILED,
            result=BrandGenerationResult(
                scraper_result=scrape_result,
                brand_data=None,
            ),
        ),
    )
