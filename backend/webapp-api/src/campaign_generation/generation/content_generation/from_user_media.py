import asyncio
import logging

from pydantic_ai import format_as_xml

import src.brand.service as brand_service
import src.campaign_generation.service as campaign_generation_job_service
from lib.db.session_factory import DbSessionFactory
from lib.prompts import PromptTemplateName
from src.brand.model import Brand
from src.campaign_generation.model import (
    CampaignGenerationJob,
    CampaignGenerationJobResult,
    ContentPlanItem,
)
from src.content.model import TextWithSingleImageContentData
from src.content_plan_item.model import ContentPlanItemUpdateRequest
from src.shared import TextWithSingleImageContentGenerator
from src.shared.model import JobStatus


logger = logging.getLogger(__name__)


async def generate_content(
    job: CampaignGenerationJob,
    session_factory: DbSessionFactory,
    content_generator: TextWithSingleImageContentGenerator,
) -> CampaignGenerationJobResult:
    if not job.result or not job.result.content_plan_items:
        raise ValueError("Content plan items not found")

    brand = await brand_service.get(session_factory, job.brand_id)
    plan_items = job.result.content_plan_items

    logger.info(f"Starting generation of {len(plan_items)} posts")

    await asyncio.gather(
        *[
            _generate_and_update_item(
                session_factory, content_generator, job.id, item, brand
            )
            for item in plan_items
        ],
        return_exceptions=False,
    )

    final_job = await campaign_generation_job_service.get(session_factory, job.id)
    if not final_job.result:
        raise ValueError("Final job result not found")
    return final_job.result


async def _generate_and_update_item(
    session_factory: DbSessionFactory,
    content_generator: TextWithSingleImageContentGenerator,
    job_id: str,
    item: ContentPlanItem,
    brand: Brand,
) -> None:
    try:
        image_url = item.image_urls[0] if item.image_urls else None
        if not image_url:
            raise ValueError(f"No image URL for item {item.id}")

        caption = await content_generator.generate_caption_for_image(
            brand_id=brand.id,
            channel=item.channel,
            caption_prompt_template_name=PromptTemplateName.TEXT_WITH_SINGLE_IMAGE_CAPTION,
            user_prompt=format_as_xml([item]),
            image_url=image_url,
        )
        update_request = ContentPlanItemUpdateRequest(
            content_data=TextWithSingleImageContentData(
                caption=caption,
                image_url=image_url,
            ),
            image_urls=[image_url],
            status=JobStatus.COMPLETED,
        )
        logger.info(f"Content generated for item {item.id}")
    except Exception as e:
        logger.error(f"Failed to generate caption for item {item.id}: {e}")
        update_request = ContentPlanItemUpdateRequest(status=JobStatus.FAILED)

    await campaign_generation_job_service.update_posting_plan_item(
        session_factory, job_id, item.id, update_request
    )
