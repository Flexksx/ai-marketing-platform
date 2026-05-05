import logging

from pydantic_ai import ImageUrl

import src.campaign_generation.service as campaign_generation_job_service
from lib.db.session_factory import DbSessionFactory
from src.campaign_generation.generation.content_brief import generate_content_brief
from src.campaign_generation.generation.content_generation import (
    generate_ai_content,
    generate_product_lifestyle_content,
    generate_user_media_content,
)
from src.campaign_generation.generation.content_plan import (
    generate_ai_content_plan,
    generate_user_media_content_plan,
)
from src.campaign_generation.model import (
    CampaignCreationJobUpdateInput,
    CampaignGenerationJob,
    CampaignGenerationJobResult,
    CampaignGenerationJobWorkflowType,
    UserMediaOnlyCampaignGenerationJobUserInput,
)
from src.shared.model import JobStatus
from src.shared.text_with_single_image import TextWithSingleImageContentGenerator


logger = logging.getLogger(__name__)


async def run(
    job: CampaignGenerationJob,
    session_factory: DbSessionFactory,
    content_generator: TextWithSingleImageContentGenerator,
) -> None:
    job_id = job.id
    try:
        logger.info(
            f"Starting campaign generation job {job_id} "
            f"with workflow type {job.workflow_type}",
            extra={"job_id": job_id},
        )

        brief_result = await _run_content_brief_step(job, session_factory)
        job = await _update_job(session_factory, job_id, brief_result)
        logger.info(
            f"Content brief completed for job {job_id}", extra={"job_id": job_id}
        )

        plan_result = await _run_content_plan_step(job, session_factory)
        job = await _update_job(session_factory, job_id, plan_result)
        logger.info(
            f"Content plan completed for job {job_id}", extra={"job_id": job_id}
        )

        generation_result = await _run_content_generation_step(
            job, session_factory, content_generator
        )
        await _update_job(
            session_factory, job_id, generation_result, status=JobStatus.COMPLETED
        )
        logger.info(
            f"Campaign generation job {job_id} completed", extra={"job_id": job_id}
        )

    except Exception as exception:
        logger.error(
            f"Campaign generation job {job_id} failed: {exception}",
            exc_info=True,
            extra={"job_id": job_id},
        )
        await _mark_job_failed(session_factory, job_id)
        raise


async def _run_content_brief_step(
    job: CampaignGenerationJob,
    session_factory: DbSessionFactory,
) -> CampaignGenerationJobResult:
    if job.workflow_type == CampaignGenerationJobWorkflowType.USER_MEDIA_ONLY:
        assert isinstance(job.user_input, UserMediaOnlyCampaignGenerationJobUserInput)
        image_urls = [ImageUrl(url=u) for u in job.user_input.image_urls]
        return await generate_content_brief(job, session_factory, image_urls=image_urls)
    return await generate_content_brief(job, session_factory)


async def _run_content_plan_step(
    job: CampaignGenerationJob,
    session_factory: DbSessionFactory,
) -> CampaignGenerationJobResult:
    if job.workflow_type == CampaignGenerationJobWorkflowType.USER_MEDIA_ONLY:
        return await generate_user_media_content_plan(job, session_factory)
    return await generate_ai_content_plan(job, session_factory)


async def _run_content_generation_step(
    job: CampaignGenerationJob,
    session_factory: DbSessionFactory,
    content_generator: TextWithSingleImageContentGenerator,
) -> CampaignGenerationJobResult:
    if job.workflow_type == CampaignGenerationJobWorkflowType.AI_GENERATED:
        return await generate_ai_content(job, session_factory, content_generator)
    if job.workflow_type == CampaignGenerationJobWorkflowType.USER_MEDIA_ONLY:
        return await generate_user_media_content(
            job, session_factory, content_generator
        )
    if job.workflow_type == CampaignGenerationJobWorkflowType.PRODUCT_LIFESTYLE:
        return await generate_product_lifestyle_content(
            job, session_factory, content_generator
        )
    raise ValueError(
        f"No content generation step for workflow type: {job.workflow_type}"
    )


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
