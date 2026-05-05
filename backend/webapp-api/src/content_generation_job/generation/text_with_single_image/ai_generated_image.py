from lib.prompts import PromptTemplateName
from src.content.model import TextWithSingleImageContentData
from src.content_generation_job.errors import (
    ContentGenerationJobInvalidUserInputException,
)
from src.content_generation_job.model import (
    AiGeneratedTextWithSingleImageContentGenerationJobUserInput,
    ContentGenerationJob,
    TextWithSingleImageContentGenerationJobResult,
)
from src.shared.text_with_single_image import TextWithSingleImageContentGenerator


async def generate_result(
    job: ContentGenerationJob,
    content_generator: TextWithSingleImageContentGenerator,
) -> TextWithSingleImageContentGenerationJobResult:
    user_input = _get_user_input_or_raise(job)
    result = await content_generator.generate_full(
        brand_id=job.brand_id,
        channel=user_input.channel,
        image_url=None,
        user_prompt=user_input.prompt,
        image_prompt_template_name=PromptTemplateName.TEXT_WITH_SINGLE_IMAGE_AI_GENERATED_IMAGE,
        caption_prompt_template_name=PromptTemplateName.TEXT_WITH_SINGLE_IMAGE_CAPTION,
    )
    return TextWithSingleImageContentGenerationJobResult(
        data=TextWithSingleImageContentData(
            caption=result.text,
            image_url=result.image_url,
        ),
        channel=user_input.channel,
        scheduled_at=user_input.scheduled_at,
    )


def _get_user_input_or_raise(
    job: ContentGenerationJob,
) -> AiGeneratedTextWithSingleImageContentGenerationJobUserInput:
    if not isinstance(
        job.user_input,
        AiGeneratedTextWithSingleImageContentGenerationJobUserInput,
    ):
        raise ContentGenerationJobInvalidUserInputException(
            job.id,
            "User input type is not valid for AI-generated image content generation job.",
        )
    return job.user_input
