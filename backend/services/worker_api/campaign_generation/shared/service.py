import logging
from abc import ABC, abstractmethod

from fastapi import Depends

from vozai.domain.campaign_generation.model import (
    CampaignGenerationJob,
    CampaignGenerationJobResult,
)
from vozai.domain.campaign_generation.schema import CampaignCreationJobUpdateInput
from vozai.domain.campaign_generation.service import CampaignGenerationJobService
from vozai.lib.job.model import JobStatus


logger = logging.getLogger(__name__)


class BaseCampaignGenerationJobRunner(ABC):
    def __init__(
        self, campaign_generation_job_service: CampaignGenerationJobService = Depends()
    ):
        self.campaign_generation_job_service = campaign_generation_job_service

    async def process(self, job_id: str) -> CampaignGenerationJob:
        try:
            job = await self.campaign_generation_job_service.get(job_id)
            job_workflow_type = job.user_input.workflow_type
            logger.info(
                f"Starting campaign generation job {job_id} with workflow type {job_workflow_type}",
                extra={"job_id": job_id},
            )
            description_result = await self.generate_content_brief(job)
            job = await self.__update_job(job_id, description_result)
            logger.info(
                f"Campaign description completed for job {job_id}",
                extra={"job_id": job_id},
            )
            posting_plan_result = await self.process_posting_plan(job)
            job = await self.__update_job(job_id, posting_plan_result)
            logger.info(
                f"Posting plan completed for job {job_id}",
                extra={"job_id": job_id},
            )
            post_generation_result = await self.process_post_generation(job)
            job = await self.__update_job(
                job_id, post_generation_result, status=JobStatus.COMPLETED
            )
            logger.info(
                f"Post generation step completed for job {job_id}",
                extra={"job_id": job_id},
            )
            logger.info(
                f"Campaign generation job {job_id} completed with status {job.status}",
                extra={"job_id": job_id},
            )
            return job
        except Exception as exception:
            logger.error(
                f"Campaign generation job {job_id} failed: {exception}",
                exc_info=True,
                extra={"job_id": job_id},
            )
            await self._mark_job_failed(job_id)
            raise

    @abstractmethod
    async def generate_content_brief(
        self, job: CampaignGenerationJob
    ) -> CampaignGenerationJobResult:
        raise NotImplementedError(
            "process_description method must be implemented by subclasses"
        )

    @abstractmethod
    async def process_posting_plan(
        self, job: CampaignGenerationJob
    ) -> CampaignGenerationJobResult:
        raise NotImplementedError(
            "process_posting_plan method must be implemented by subclasses"
        )

    @abstractmethod
    async def process_post_generation(
        self, job: CampaignGenerationJob
    ) -> CampaignGenerationJobResult:
        raise NotImplementedError(
            "process_post_generation method must be implemented by subclasses"
        )

    async def __update_job(
        self,
        job_id: str,
        result: CampaignGenerationJobResult,
        status: JobStatus = JobStatus.IN_PROGRESS,
    ) -> CampaignGenerationJob:
        return await self.campaign_generation_job_service.update(
            job_id=job_id,
            request=CampaignCreationJobUpdateInput(
                status=status,
                result=result,
            ),
        )

    async def _mark_job_failed(self, job_id: str) -> None:
        try:
            await self.campaign_generation_job_service.update(
                job_id=job_id,
                request=CampaignCreationJobUpdateInput(
                    status=JobStatus.FAILED,
                    result=None,
                ),
            )
        except Exception as update_error:
            logger.error(
                f"Failed to update job {job_id} status to FAILED: {update_error}",
                extra={"job_id": job_id},
            )
