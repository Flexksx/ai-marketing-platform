import asyncio
import logging
from collections.abc import Awaitable

from pydantic_ai import format_as_xml

import src.brand.service as brand_service
import src.campaign_generation.service as campaign_generation_job_service
from lib.content_generation import text_with_single_image
from lib.model import JobStatus
from lib.prompts import PromptTemplateName
from src.campaign_generation.model import (
    CampaignGenerationJob,
    CampaignGenerationJobResult,
    ContentPlanItem,
)
from src.content.model import TextWithSingleImageContentData
from src.content_plan_item.model import ContentPlanItemUpdateRequest


logger = logging.getLogger(__name__)


async def generate_ai_content(job: CampaignGenerationJob) -> CampaignGenerationJobResult:
    plan_items = _get_plan_items_or_raise(job)
    await asyncio.gather(
        *[
            _generate_and_update_item(
                job.id,
                item,
                _build_ai_generated_update_request(job.brand_id, item),
            )
            for item in plan_items
        ]
    )
    return await _collect_final_result(job.id)


async def generate_user_media_content(job: CampaignGenerationJob) -> CampaignGenerationJobResult:
    brand = await brand_service.get(job.brand_id)
    plan_items = _get_plan_items_or_raise(job)
    await asyncio.gather(
        *[
            _generate_and_update_item(
                job.id,
                item,
                _build_user_media_update_request(brand.id, item),
            )
            for item in plan_items
        ]
    )
    return await _collect_final_result(job.id)


async def generate_product_lifestyle_content(job: CampaignGenerationJob) -> CampaignGenerationJobResult:
    plan_items = _get_plan_items_or_raise(job)
    product_image_urls: list[str] = getattr(job.user_input, "image_urls", []) or []
    await asyncio.gather(
        *[
            _generate_and_update_item(
                job.id,
                item,
                _build_product_lifestyle_update_request(
                    index, item, job.brand_id, product_image_urls
                ),
            )
            for index, item in enumerate(plan_items)
        ]
    )
    return await _collect_final_result(job.id)


def _get_plan_items_or_raise(job: CampaignGenerationJob) -> list[ContentPlanItem]:
    if not job.result or not job.result.content_plan_items:
        raise ValueError("Content plan items not found")
    return job.result.content_plan_items


async def _generate_and_update_item(
    job_id: str,
    item: ContentPlanItem,
    update_request_coro: Awaitable[ContentPlanItemUpdateRequest],
) -> None:
    try:
        update_request = await update_request_coro
    except Exception as e:
        logger.error(f"Failed to generate item {item.id}: {e}")
        update_request = ContentPlanItemUpdateRequest(status=JobStatus.FAILED)
    await campaign_generation_job_service.update_posting_plan_item(
        job_id, item.id, update_request
    )


async def _collect_final_result(job_id: str) -> CampaignGenerationJobResult:
    final_job = await campaign_generation_job_service.get(job_id)
    if not final_job.result:
        raise ValueError("Final job result not found")
    return final_job.result


async def _build_ai_generated_update_request(
    brand_id: str,
    item: ContentPlanItem,
) -> ContentPlanItemUpdateRequest:
    result = await text_with_single_image.generate_full(
        brand_id=brand_id,
        channel=item.channel,
        image_prompt_template_name=PromptTemplateName.TEXT_WITH_SINGLE_IMAGE_AI_GENERATED_IMAGE,
        caption_prompt_template_name=PromptTemplateName.TEXT_WITH_SINGLE_IMAGE_CAPTION,
        user_prompt=format_as_xml(item),
        image_url=None,
    )
    return ContentPlanItemUpdateRequest(
        content_data=TextWithSingleImageContentData(
            caption=result.text,
            image_url=result.image_url,
        ),
        image_urls=[result.image_url],
        status=JobStatus.COMPLETED,
    )


async def _build_user_media_update_request(
    brand_id: str,
    item: ContentPlanItem,
) -> ContentPlanItemUpdateRequest:
    image_url = item.image_urls[0] if item.image_urls else None
    if not image_url:
        raise ValueError(f"No image URL for item {item.id}")
    caption = await text_with_single_image.generate_caption_for_image(
        brand_id=brand_id,
        channel=item.channel,
        caption_prompt_template_name=PromptTemplateName.TEXT_WITH_SINGLE_IMAGE_CAPTION,
        user_prompt=format_as_xml([item]),
        image_url=image_url,
    )
    return ContentPlanItemUpdateRequest(
        content_data=TextWithSingleImageContentData(
            caption=caption,
            image_url=image_url,
        ),
        image_urls=[image_url],
        status=JobStatus.COMPLETED,
    )


async def _build_product_lifestyle_update_request(
    index: int,
    item: ContentPlanItem,
    brand_id: str,
    product_image_urls: list[str],
) -> ContentPlanItemUpdateRequest:
    product_image_url = (
        product_image_urls[index % len(product_image_urls)]
        if product_image_urls
        else None
    )
    result = await text_with_single_image.generate_full(
        brand_id=brand_id,
        channel=item.channel,
        image_prompt_template_name=PromptTemplateName.TEXT_WITH_SINGLE_IMAGE_PRODUCT_LIFESTYLE_IMAGE,
        caption_prompt_template_name=PromptTemplateName.TEXT_WITH_SINGLE_IMAGE_CAPTION,
        user_prompt=format_as_xml(item),
        image_url=product_image_url,
    )
    return ContentPlanItemUpdateRequest(
        content_data=TextWithSingleImageContentData(
            caption=result.text,
            image_url=result.image_url,
        ),
        image_urls=[result.image_url],
        status=JobStatus.COMPLETED,
    )
