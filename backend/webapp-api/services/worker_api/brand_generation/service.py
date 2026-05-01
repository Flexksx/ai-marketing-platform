import logging

from fastapi import Depends

from services.worker_api.brand_generation.steps.data_extraction import (
    BrandDataExtractionStep,
)
from services.worker_api.brand_generation.steps.scraping import BrandScrapingStep
from vozai.domain.brand_extraction.model import (
    BrandGenerationJob,
    BrandGenerationResult,
)
from vozai.domain.brand_extraction.schema import (
    BrandGenerationJobUpdateRequest,
)
from vozai.domain.brand_extraction.service import BrandGenerationJobService
from vozai.lib.job.model import JobStatus


logger = logging.getLogger(__name__)


class BrandGenerationJobRunner:
    def __init__(
        self,
        service: BrandGenerationJobService = Depends(),
        scraping_step: BrandScrapingStep = Depends(),
        data_extraction_step: BrandDataExtractionStep = Depends(),
    ):
        self.service = service
        self.scraping_step = scraping_step
        self.data_extraction_step = data_extraction_step

    async def _update_job(
        self,
        job_id: str,
        status: JobStatus,
        result: BrandGenerationResult,
    ) -> BrandGenerationJob:
        return await self.service.update(
            job_id=job_id,
            request=BrandGenerationJobUpdateRequest(status=status, result=result),
        )

    async def process(self, job_id: str) -> BrandGenerationJob:
        try:
            job = await self.service.get(job_id)

            if job.result:
                await self._update_job(job_id, JobStatus.IN_PROGRESS, job.result)
            logger.info(
                f"Job {job_id} status updated to IN_PROGRESS",
                extra={"job_id": job_id},
            )

            logger.info(
                f"Processing scraping step for job {job_id}",
                extra={"job_id": job_id},
            )
            scraping_result = await self.scraping_step.execute(job)
            job = await self._update_job(job_id, JobStatus.IN_PROGRESS, scraping_result)
            logger.info(
                f"Scraping step completed for job {job_id}",
                extra={"job_id": job_id},
            )

            logger.info(
                f"Processing data extraction step for job {job_id}",
                extra={"job_id": job_id},
            )
            data_extraction_result = await self.data_extraction_step.execute(job)
            job = await self._update_job(
                job_id, JobStatus.COMPLETED, data_extraction_result
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
            await self._mark_job_failed(job_id)
            raise

    async def _mark_job_failed(self, job_id: str) -> None:
        job = await self.service.get(job_id)
        scrape_result = job.result.scraper_result if job.result else None
        await self.service.update(
            job_id=job_id,
            request=BrandGenerationJobUpdateRequest(
                status=JobStatus.FAILED,
                result=BrandGenerationResult(
                    scraper_result=scrape_result,
                    brand_data=None,
                ),
            ),
        )
