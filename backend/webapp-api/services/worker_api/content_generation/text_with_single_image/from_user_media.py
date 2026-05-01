from fastapi import Depends
from pydantic import BaseModel, ConfigDict
from pydantic_ai import Agent, ImageUrl, RunContext

from services.worker_api.content_generation.text_with_single_image.base_strategy import (
    BaseTextWithSingleImageContentGenerationJobStrategy,
)
from aimarketing.domain.brand import Brand, BrandService
from aimarketing.domain.content import TextWithSingleImageContentData
from aimarketing.domain.content_channel import ContentChannelName
from aimarketing.domain.content_generation_job import (
    ContentGenerationJob,
    ContentGenerationJobInvalidUserInputException,
    FromUserMediaTextWithSingleImageContentGenerationJobUserInput,
    TextWithSingleImageContentGenerationJobResult,
)
from aimarketing.lib.ai_agents.schema import PydanticAiModel
from aimarketing.lib.prompts import PromptService, PromptTemplateName


class _AgentDependencies(BaseModel):
    brand: Brand
    channel: ContentChannelName


class _AgentOutputFromUserMedia(BaseModel):
    caption: str

    model_config = ConfigDict(from_attributes=True)


class FromUserMediaTextWithSingleImageContentGenerationJobStrategy(
    BaseTextWithSingleImageContentGenerationJobStrategy
):
    def __init__(
        self,
        brand_service: BrandService = Depends(),
        prompt_service: PromptService = Depends(),
    ):
        self.brand_service = brand_service
        self.prompt_service = prompt_service
        self.__agent = Agent(
            model=PydanticAiModel.GEMINI_FLASH_LATEST,
            deps_type=_AgentDependencies,
            output_type=_AgentOutputFromUserMedia,
        )

        @self.__agent.system_prompt
        def get_system_prompt(context: RunContext[_AgentDependencies]):
            return self.prompt_service.render(
                PromptTemplateName.TEXT_WITH_SINGLE_IMAGE_CAPTION,
                context.deps.model_dump(),
            )

    async def generate(
        self, job: ContentGenerationJob
    ) -> TextWithSingleImageContentGenerationJobResult:
        user_input = self.__get_from_user_media_user_input_or_raise(job)
        brand: Brand = await self.brand_service.get(job.brand_id)
        agent_dependencies = _AgentDependencies(brand=brand, channel=user_input.channel)
        agent_run = await self.__agent.run(
            user_prompt=[
                user_input.prompt,
                ImageUrl(url=user_input.image_url),
            ],
            deps=agent_dependencies,
        )
        result: _AgentOutputFromUserMedia = agent_run.output  # ty:ignore[invalid-assignment]
        return TextWithSingleImageContentGenerationJobResult(
            data=TextWithSingleImageContentData(
                caption=result.caption,
                image_url=user_input.image_url,
            ),
            channel=user_input.channel,
            scheduled_at=user_input.scheduled_at,
        )

    def __get_from_user_media_user_input_or_raise(
        self, job: ContentGenerationJob
    ) -> FromUserMediaTextWithSingleImageContentGenerationJobUserInput:
        if not isinstance(
            job.user_input,
            FromUserMediaTextWithSingleImageContentGenerationJobUserInput,
        ):
            raise ContentGenerationJobInvalidUserInputException(
                job.id,
                "User input type is not valid for text with single image content generation job.",
            )
        return job.user_input
