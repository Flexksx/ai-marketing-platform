import logging
from collections.abc import Awaitable, Callable

import src.content_generation_job.service as content_generation_job_service
from lib.db.session_factory import DbSessionFactory
from src.content_generation_job.errors import ContentGenerationJobRuntimeException
from src.content_generation_job.model import (
    ContentGenerationJob,
    ContentGenerationJobResult,
    ContentGenerationJobUpdateRequest,
)
from src.shared.model import JobStatus


logger = logging.getLogger(__name__)


async def run_content_generation_job(
    session_factory: DbSessionFactory,
    job_id: str,
    generate: Callable[[ContentGenerationJob], Awaitable[ContentGenerationJobResult]],
) -> ContentGenerationJob:
    try:
        logger.info(
            f"Starting content generation job {job_id}",
            extra={"job_id": job_id},
        )
        job = await content_generation_job_service.get(session_factory, job_id)
        result = await generate(job)
        logger.info(
            f"Content generation result produced for job {job_id}",
            extra={"job_id": job_id},
        )
        completed_job = await _complete_job(session_factory, job_id, result)
        logger.info(
            f"Content generation job {job_id} marked as completed "
            f"with status {completed_job.status}",
            extra={"job_id": job_id},
        )
        return completed_job
    except Exception as e:
        await _mark_job_failed(session_factory, job_id)
        raise ContentGenerationJobRuntimeException(job_id, e) from e


async def _complete_job(
    session_factory: DbSessionFactory,
    job_id: str,
    result: ContentGenerationJobResult,
) -> ContentGenerationJob:
    return await content_generation_job_service.update(
        session_factory,
        job_id,
        ContentGenerationJobUpdateRequest(
            status=JobStatus.COMPLETED,
            result=result,
        ),
    )


async def _mark_job_failed(
    session_factory: DbSessionFactory,
    job_id: str,
) -> ContentGenerationJob:
    return await content_generation_job_service.update(
        session_factory,
        job_id,
        ContentGenerationJobUpdateRequest(
            status=JobStatus.FAILED,
            result=None,
        ),
    )
