import logging
from abc import ABC, abstractmethod

import public
from fastapi import Depends

from lib.db.session_factory import DbSessionFactory
import src.content_generation_job.service as content_generation_job_service
from webapp_api_contract.content_generation import (
    ContentGenerationJobResult,
    ContentGenerationJobRuntimeException,
    ContentGenerationJobUpdateRequest,
)
from webapp_api_contract.content_generation import ContentGenerationJob
from webapp_api_contract.shared import JobStatus


logger = logging.getLogger(__name__)


@public.add
class BaseContentGenerationJobRunner(ABC):
    def __init__(self, session_factory: DbSessionFactory = Depends()):
        self.session_factory = session_factory

    async def process(self, job_id: str) -> ContentGenerationJob:
        try:
            logger.info(
                f"Starting content generation job {job_id}",
                extra={"job_id": job_id},
            )
            job = await content_generation_job_service.get(
                self.session_factory,
                job_id,
            )
            result = await self.generate_result(job)
            logger.info(
                f"Content generation result produced for job {job_id}",
                extra={"job_id": job_id},
            )
            completed_job = await self.__complete_job(job_id, result)
            logger.info(
                f"Content generation job {job_id} marked as completed "
                f"with status {completed_job.status}",
                extra={"job_id": job_id},
            )
            return completed_job
        except Exception as e:
            await self._mark_job_failed(job_id)
            raise ContentGenerationJobRuntimeException(job_id, e) from e

    @abstractmethod
    async def generate_result(
        self, job: ContentGenerationJob
    ) -> ContentGenerationJobResult:
        raise NotImplementedError(
            "generate_result method must be implemented by subclasses"
        )

    async def __complete_job(
        self, job_id: str, result: ContentGenerationJobResult
    ) -> ContentGenerationJob:
        return await content_generation_job_service.update(
            self.session_factory,
            job_id,
            ContentGenerationJobUpdateRequest(
                status=JobStatus.COMPLETED,
                result=result,
            ),
        )

    async def _mark_job_failed(self, job_id: str) -> ContentGenerationJob:
        return await content_generation_job_service.update(
            self.session_factory,
            job_id,
            ContentGenerationJobUpdateRequest(
                status=JobStatus.FAILED,
                result=None,
            ),
        )
