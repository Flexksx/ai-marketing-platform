from lib.prompts import PromptTemplateName
from src.content.model import TextWithSingleImageContentData
from src.content_generation_job.errors import (
    ContentGenerationJobInvalidUserInputException,
)
from src.content_generation_job.model import (
    ContentGenerationJob,
    ProductLifestyleTextWithSingleImageContentGenerationJobUserInput,
    TextWithSingleImageContentGenerationJobResult,
)
from src.shared import TextWithSingleImageContentGenerator


async def generate_result(
    job: ContentGenerationJob,
    content_generator: TextWithSingleImageContentGenerator,
) -> TextWithSingleImageContentGenerationJobResult:
    user_input = _get_user_input_or_raise(job)
    result = await content_generator.generate_full(
        brand_id=job.brand_id,
        image_url=user_input.image_url,
        image_prompt_template_name=PromptTemplateName.TEXT_WITH_SINGLE_IMAGE_PRODUCT_LIFESTYLE_IMAGE,
        caption_prompt_template_name=PromptTemplateName.TEXT_WITH_SINGLE_IMAGE_CAPTION,
        channel=user_input.channel,
        user_prompt=user_input.prompt,
    )
    return TextWithSingleImageContentGenerationJobResult(
        data=TextWithSingleImageContentData(
            image_url=result.image_url,
            caption=result.text,
        ),
        channel=result.channel,
        scheduled_at=user_input.scheduled_at,
    )


def _get_user_input_or_raise(
    job: ContentGenerationJob,
) -> ProductLifestyleTextWithSingleImageContentGenerationJobUserInput:
    if not isinstance(
        job.user_input,
        ProductLifestyleTextWithSingleImageContentGenerationJobUserInput,
    ):
        raise ContentGenerationJobInvalidUserInputException(
            job.id,
            "User input type is not valid for product lifestyle content generation job.",
        )
    return job.user_input
