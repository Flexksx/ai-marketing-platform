from pydantic import BaseModel, ConfigDict
from pydantic_ai import Agent, ImageUrl, RunContext

import src.brand.service as brand_service
from lib.ai_agents.schema import PydanticAiModel
from lib.db.session_factory import DbSessionFactory
from lib.prompts import PromptService, PromptTemplateName
from src.brand.model import Brand
from src.content.model import TextWithSingleImageContentData
from src.content_generation_job.errors import (
    ContentGenerationJobInvalidUserInputException,
)
from src.content_generation_job.model import (
    AiGeneratedTextWithSingleImageContentGenerationJobUserInput,
    ContentGenerationJob,
    FromUserMediaTextWithSingleImageContentGenerationJobUserInput,
    ProductLifestyleTextWithSingleImageContentGenerationJobUserInput,
    TextWithSingleImageContentGenerationJobResult,
)
from src.shared import text_with_single_image
from src.shared.model import ContentChannelName
from src.shared.text_with_single_image import TextWithSingleImageDeps


class _FromUserMediaAgentDependencies(BaseModel):
    brand: Brand
    channel: ContentChannelName


class _FromUserMediaAgentOutput(BaseModel):
    caption: str

    model_config = ConfigDict(from_attributes=True)


_prompt_service = PromptService()

_from_user_media_agent: Agent[
    _FromUserMediaAgentDependencies, _FromUserMediaAgentOutput
] = Agent(
    model=PydanticAiModel.GEMINI_FLASH_LATEST,
    deps_type=_FromUserMediaAgentDependencies,
    output_type=_FromUserMediaAgentOutput,
)


@_from_user_media_agent.system_prompt
def _get_from_user_media_system_prompt(
    context: RunContext[_FromUserMediaAgentDependencies],
) -> str:
    return _prompt_service.render(
        PromptTemplateName.TEXT_WITH_SINGLE_IMAGE_CAPTION,
        context.deps.model_dump(),
    )


async def generate_from_user_media_result(
    job: ContentGenerationJob,
    session_factory: DbSessionFactory,
) -> TextWithSingleImageContentGenerationJobResult:
    user_input = _get_from_user_media_input_or_raise(job)
    brand: Brand = await brand_service.get(session_factory, job.brand_id)
    agent_run = await _from_user_media_agent.run(
        user_prompt=[
            user_input.prompt,
            ImageUrl(url=user_input.image_url),
        ],
        deps=_FromUserMediaAgentDependencies(brand=brand, channel=user_input.channel),
    )
    result: _FromUserMediaAgentOutput = agent_run.output
    return TextWithSingleImageContentGenerationJobResult(
        data=TextWithSingleImageContentData(
            caption=result.caption,
            image_url=user_input.image_url,
        ),
        channel=user_input.channel,
        scheduled_at=user_input.scheduled_at,
    )


async def generate_ai_image_result(
    job: ContentGenerationJob,
    content_deps: TextWithSingleImageDeps,
) -> TextWithSingleImageContentGenerationJobResult:
    user_input = _get_ai_generated_input_or_raise(job)
    result = await text_with_single_image.generate_full(
        content_deps,
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


async def generate_product_lifestyle_result(
    job: ContentGenerationJob,
    content_deps: TextWithSingleImageDeps,
) -> TextWithSingleImageContentGenerationJobResult:
    user_input = _get_product_lifestyle_input_or_raise(job)
    result = await text_with_single_image.generate_full(
        content_deps,
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


def _get_from_user_media_input_or_raise(
    job: ContentGenerationJob,
) -> FromUserMediaTextWithSingleImageContentGenerationJobUserInput:
    if not isinstance(
        job.user_input,
        FromUserMediaTextWithSingleImageContentGenerationJobUserInput,
    ):
        raise ContentGenerationJobInvalidUserInputException(
            job.id,
            "User input type is not valid for from-user-media content generation job.",
        )
    return job.user_input


def _get_ai_generated_input_or_raise(
    job: ContentGenerationJob,
) -> AiGeneratedTextWithSingleImageContentGenerationJobUserInput:
    if not isinstance(
        job.user_input,
        AiGeneratedTextWithSingleImageContentGenerationJobUserInput,
    ):
        raise ContentGenerationJobInvalidUserInputException(
            job.id,
            "User input is not valid for AI-generated image content generation job.",
        )
    return job.user_input


def _get_product_lifestyle_input_or_raise(
    job: ContentGenerationJob,
) -> ProductLifestyleTextWithSingleImageContentGenerationJobUserInput:
    if not isinstance(
        job.user_input,
        ProductLifestyleTextWithSingleImageContentGenerationJobUserInput,
    ):
        raise ContentGenerationJobInvalidUserInputException(
            job.id,
            "User input is not valid for product lifestyle content generation job.",
        )
    return job.user_input
