import asyncio
import logging

from pydantic_ai import format_as_xml

import src.campaign_generation.service as campaign_generation_job_service
from lib.db.session_factory import DbSessionFactory
from lib.prompts import PromptTemplateName
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

    plan_items = job.result.content_plan_items
    product_image_urls = _get_product_image_urls(job)

    logger.info(
        f"Generating {len(plan_items)} product lifestyle posts "
        f"with {len(product_image_urls)} product images"
    )

    await asyncio.gather(
        *[
            _generate_and_update_item(
                session_factory, content_generator, job, index, item, product_image_urls
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
    content_generator: TextWithSingleImageContentGenerator,
    job: CampaignGenerationJob,
    item_index: int,
    item: ContentPlanItem,
    product_image_urls: list[str],
) -> None:
    try:
        product_image_url = _select_product_image(product_image_urls, item_index)
        result = await content_generator.generate_full(
            brand_id=job.brand_id,
            channel=item.channel,
            image_prompt_template_name=PromptTemplateName.TEXT_WITH_SINGLE_IMAGE_PRODUCT_LIFESTYLE_IMAGE,
            caption_prompt_template_name=PromptTemplateName.TEXT_WITH_SINGLE_IMAGE_CAPTION,
            user_prompt=format_as_xml(item),
            image_url=product_image_url,
        )
        update_request = ContentPlanItemUpdateRequest(
            content_data=TextWithSingleImageContentData(
                caption=result.text,
                image_url=result.image_url,
            ),
            image_urls=[result.image_url],
            status=JobStatus.COMPLETED,
        )
        logger.info(f"Product lifestyle item {item.id} completed")
    except Exception as e:
        logger.error(f"Failed to generate item {item.id}: {e}")
        update_request = ContentPlanItemUpdateRequest(status=JobStatus.FAILED)

    await campaign_generation_job_service.update_posting_plan_item(
        session_factory, job.id, item.id, update_request
    )


def _get_product_image_urls(job: CampaignGenerationJob) -> list[str]:
    image_urls = getattr(job.user_input, "image_urls", None)
    return image_urls if image_urls else []


def _select_product_image(product_image_urls: list[str], item_index: int) -> str | None:
    if not product_image_urls:
        return None
    return product_image_urls[item_index % len(product_image_urls)]
