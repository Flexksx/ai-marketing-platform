import logging

from fastapi import APIRouter, BackgroundTasks, Body, Depends
from pydantic import BaseModel

from services.worker_api.campaign_generation.errors import (
    CampaignGenerationJobProcessingFailureException,
)
from services.worker_api.campaign_generation.factory import (
    CampaignGenerationJobRunnerFactory,
)
from services.worker_api.campaign_generation.shared.service import (
    BaseCampaignGenerationJobRunner,
)
from aimarketing.config import Settings, get_settings
from aimarketing.domain.campaign_generation import (
    CampaignGenerationJobService,
)
from aimarketing.lib.cloudtasks.schema import (
    CampaignGenerationTaskPayload,
)


SUCCESS_STATUS = "success"


class CampaignGenerationTaskResponse(BaseModel):
    status: str
    job_id: str


router = APIRouter(prefix="/tasks", tags=["tasks"])

logger = logging.getLogger(__name__)


@router.post("/campaign-generation")
async def start(
    background_tasks: BackgroundTasks,
    payload: CampaignGenerationTaskPayload = Body(...),  # noqa: B008
    factory: CampaignGenerationJobRunnerFactory = Depends(),
    campaign_service: CampaignGenerationJobService = Depends(),
    settings: Settings = Depends(get_settings),
):
    job_id = payload.job_id

    logger.info(
        f"Received campaign generation task for job {job_id}",
        extra={"job_id": job_id},
    )

    # Get the job to determine workflow type
    job = await campaign_service.get(job_id)
    runner = factory.get_runner(job.workflow_type)

    runner_name = type(runner).__name__
    logger.info(
        f"Using {runner_name} for job {job_id} with workflow type {job.workflow_type}",
        extra={"job_id": job_id},
    )

    is_local = settings.gcp_project_id == "local-dev"

    if is_local:
        return await __process_task_locally(background_tasks, runner, job_id)
    return await __process_task_on_google_cloud_tasks(runner, job_id)


async def __process_task_locally(
    background_tasks: BackgroundTasks,
    processor: BaseCampaignGenerationJobRunner,
    job_id: str,
):
    background_tasks.add_task(processor.process, job_id)
    return CampaignGenerationTaskResponse(status=SUCCESS_STATUS, job_id=job_id)


async def __process_task_on_google_cloud_tasks(
    processor: BaseCampaignGenerationJobRunner,
    job_id: str,
):
    try:
        await processor.process(job_id)
        return CampaignGenerationTaskResponse(status=SUCCESS_STATUS, job_id=job_id)
    except Exception as e:
        raise CampaignGenerationJobProcessingFailureException(job_id, e) from e
