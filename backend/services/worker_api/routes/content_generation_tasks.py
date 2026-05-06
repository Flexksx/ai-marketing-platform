import logging

from fastapi import APIRouter, BackgroundTasks, Body, Depends
from pydantic import BaseModel

from services.worker_api.content_generation.factory import (
    ContentGenerationJobRunnerFactory,
)
from services.worker_api.content_generation.shared.service import (
    BaseContentGenerationJobRunner,
)
from vozai.config import Settings, get_settings
from vozai.domain.content_generation_job import (
    ContentGenerationJobService,
)
from vozai.lib.cloudtasks.schema import (
    ContentGenerationTaskPayload,
)


SUCCESS_STATUS = "success"


class ContentGenerationTaskResponse(BaseModel):
    status: str
    job_id: str


router = APIRouter(prefix="/tasks", tags=["tasks"])

logger = logging.getLogger(__name__)


@router.post("/content-generation", response_model=ContentGenerationTaskResponse)
async def start(
    background_tasks: BackgroundTasks,
    payload: ContentGenerationTaskPayload = Body(...),  # noqa: B008
    factory: ContentGenerationJobRunnerFactory = Depends(),
    content_service: ContentGenerationJobService = Depends(),
    settings: Settings = Depends(get_settings),
) -> ContentGenerationTaskResponse:
    job_id = payload.job_id

    logger.info(
        f"Received content generation task for job {job_id}",
        extra={"job_id": job_id},
    )

    job = await content_service.get(job_id)
    runner = factory.get_runner(job)

    runner_name = type(runner).__name__
    logger.info(
        f"Using {runner_name} for job {job_id} with worfklow type {job.user_input.workflow_type}",
        extra={"job_id": job_id},
    )

    is_local = settings.gcp_project_id == "local-dev"

    if is_local:
        return await __process_task_locally(background_tasks, runner, job_id)
    return await __process_task_on_google_cloud_tasks(runner, job_id)


async def __process_task_locally(
    background_tasks: BackgroundTasks,
    processor: BaseContentGenerationJobRunner,
    job_id: str,
):
    background_tasks.add_task(processor.process, job_id)
    return ContentGenerationTaskResponse(status=SUCCESS_STATUS, job_id=job_id)


async def __process_task_on_google_cloud_tasks(
    processor: BaseContentGenerationJobRunner,
    job_id: str,
):
    try:
        await processor.process(job_id)
        return ContentGenerationTaskResponse(status=SUCCESS_STATUS, job_id=job_id)
    except Exception as e:
        logger.error(
            f"Failed to process content generation job {job_id}: {e}",
            extra={"job_id": job_id},
        )
        raise
