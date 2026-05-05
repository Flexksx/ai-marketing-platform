import logging

from pydantic_ai import format_as_xml

import src.brand.service as brand_service
from lib.db.session_factory import DbSessionFactory
from lib.prompts import PromptTemplateName
from src.campaign_generation.generation.content_generation.service import (
    generate_content_for_plan_items,
)
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
    brand = await brand_service.get(session_factory, job.brand_id)

    async def generate_item(
        _index: int, item: ContentPlanItem
    ) -> ContentPlanItemUpdateRequest:
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
        return ContentPlanItemUpdateRequest(
            content_data=TextWithSingleImageContentData(
                caption=caption,
                image_url=image_url,
            ),
            image_urls=[image_url],
            status=JobStatus.COMPLETED,
        )

    return await generate_content_for_plan_items(session_factory, job, generate_item)
