import asyncio
import logging
from collections.abc import Awaitable, Callable

import src.campaign_generation.service as campaign_generation_job_service
from lib.db.session_factory import DbSessionFactory
from src.campaign_generation.model import (
    CampaignGenerationJob,
    CampaignGenerationJobResult,
    ContentPlanItem,
)
from src.content_plan_item.model import ContentPlanItemUpdateRequest
from src.shared.model import JobStatus


logger = logging.getLogger(__name__)


async def generate_content_for_plan_items(
    session_factory: DbSessionFactory,
    job: CampaignGenerationJob,
    generate_item: Callable[
        [int, ContentPlanItem], Awaitable[ContentPlanItemUpdateRequest]
    ],
) -> CampaignGenerationJobResult:
    if not job.result or not job.result.content_plan_items:
        raise ValueError("Content plan items not found")
    plan_items = job.result.content_plan_items
    await asyncio.gather(
        *[
            _generate_and_update_item(
                session_factory, job.id, index, item, generate_item
            )
            for index, item in enumerate(plan_items)
        ],
        return_exceptions=False,
    )
    final_job = await campaign_generation_job_service.get(session_factory, job.id)
    if not final_job.result:
        raise ValueError("Final job result not found")
    return final_job.result


async def _generate_and_update_item(
    session_factory: DbSessionFactory,
    job_id: str,
    index: int,
    item: ContentPlanItem,
    generate: Callable[[int, ContentPlanItem], Awaitable[ContentPlanItemUpdateRequest]],
) -> None:
    try:
        update_request = await generate(index, item)
    except Exception as e:
        logger.error(f"Failed to generate item {item.id}: {e}")
        update_request = ContentPlanItemUpdateRequest(status=JobStatus.FAILED)
    await campaign_generation_job_service.update_posting_plan_item(
        session_factory, job_id, item.id, update_request
    )
