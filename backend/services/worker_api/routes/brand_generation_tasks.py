import logging

from fastapi import APIRouter, BackgroundTasks, Body, Depends

from services.worker_api.brand_generation.service import (
    BrandGenerationJobRunner,
)
from vozai.config import get_settings
from vozai.lib.cloudtasks.schema import (
    BrandGenerationTaskPayload,
)


router = APIRouter(prefix="/tasks", tags=["tasks"])

logger = logging.getLogger(__name__)


@router.post("/brand-generation")
async def process_brand_generation(
    background_tasks: BackgroundTasks,
    payload: BrandGenerationTaskPayload = Body(...),  # noqa: B008
    processor: BrandGenerationJobRunner = Depends(),
):
    job_id = payload.job_id
    settings = get_settings()

    logger.info(
        f"Received brand generation task for job {job_id}",
        extra={"job_id": job_id},
    )

    is_local = settings.gcp_project_id == "local-dev"

    if is_local:
        background_tasks.add_task(processor.process, job_id)
        return {"status": "accepted", "job_id": job_id}
    await processor.process(job_id)
    logger.info(
        f"✓ Successfully processed brand generation job {job_id}",
        extra={"job_id": job_id},
    )
    return {"status": "success", "job_id": job_id}
