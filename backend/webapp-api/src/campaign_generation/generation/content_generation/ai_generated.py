from pydantic_ai import format_as_xml

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


async def generate_content(
    job: CampaignGenerationJob,
    session_factory: DbSessionFactory,
    content_generator: TextWithSingleImageContentGenerator,
) -> CampaignGenerationJobResult:
    async def generate_item(
        _index: int, item: ContentPlanItem
    ) -> ContentPlanItemUpdateRequest:
        result = await content_generator.generate_full(
            brand_id=job.brand_id,
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

    return await generate_content_for_plan_items(session_factory, job, generate_item)
