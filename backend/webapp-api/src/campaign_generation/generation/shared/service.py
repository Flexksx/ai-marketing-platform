import logging
from collections.abc import Awaitable, Callable

import src.campaign_generation.service as campaign_generation_job_service
from lib.db.session_factory import DbSessionFactory
from src.campaign_generation.model import (
    CampaignCreationJobUpdateInput,
    CampaignGenerationJob,
    CampaignGenerationJobResult,
)
from src.shared.model import JobStatus


logger = logging.getLogger(__name__)


async def run_campaign_generation_job(
    session_factory: DbSessionFactory,
    job_id: str,
    generate_content_brief: Callable[
        [CampaignGenerationJob], Awaitable[CampaignGenerationJobResult]
    ],
    process_posting_plan: Callable[
        [CampaignGenerationJob], Awaitable[CampaignGenerationJobResult]
    ],
    process_post_generation: Callable[
        [CampaignGenerationJob], Awaitable[CampaignGenerationJobResult]
    ],
) -> CampaignGenerationJob:
    try:
        job = await campaign_generation_job_service.get(session_factory, job_id)
        logger.info(
            f"Starting campaign generation job {job_id} with workflow type {job.user_input.workflow_type}",
            extra={"job_id": job_id},
        )
        description_result = await generate_content_brief(job)
        job = await _update_job(session_factory, job_id, description_result)
        logger.info(
            f"Campaign description completed for job {job_id}", extra={"job_id": job_id}
        )

        posting_plan_result = await process_posting_plan(job)
        job = await _update_job(session_factory, job_id, posting_plan_result)
        logger.info(
            f"Posting plan completed for job {job_id}", extra={"job_id": job_id}
        )

        post_generation_result = await process_post_generation(job)
        job = await _update_job(
            session_factory, job_id, post_generation_result, status=JobStatus.COMPLETED
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
        await _mark_job_failed(session_factory, job_id)
        raise


async def _update_job(
    session_factory: DbSessionFactory,
    job_id: str,
    result: CampaignGenerationJobResult,
    status: JobStatus = JobStatus.IN_PROGRESS,
) -> CampaignGenerationJob:
    return await campaign_generation_job_service.update(
        session_factory,
        job_id,
        CampaignCreationJobUpdateInput(status=status, result=result),
    )


async def _mark_job_failed(
    session_factory: DbSessionFactory,
    job_id: str,
) -> None:
    try:
        await campaign_generation_job_service.update(
            session_factory,
            job_id,
            CampaignCreationJobUpdateInput(status=JobStatus.FAILED, result=None),
        )
    except Exception as update_error:
        logger.error(
            f"Failed to update job {job_id} status to FAILED: {update_error}",
            extra={"job_id": job_id},
        )
