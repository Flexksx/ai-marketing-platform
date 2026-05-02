from fastapi import Depends
from pydantic import BaseModel, ConfigDict
from pydantic_ai import Agent, ImageUrl, RunContext

import src.brands.service as brand_service
from lib.ai_agents.schema import PydanticAiModel
from lib.db.session_factory import DbSessionFactory
from lib.prompts import PromptService, PromptTemplateName
from src.content_generation_job.generation.text_with_single_image import base_strategy
from webapp_api_contract.brands import Brand
from webapp_api_contract.content import TextWithSingleImageContentData
from webapp_api_contract.content_generation import (
    ContentGenerationJob,
    ContentGenerationJobInvalidUserInputException,
    FromUserMediaTextWithSingleImageContentGenerationJobUserInput,
    TextWithSingleImageContentGenerationJobResult,
)
from webapp_api_contract.shared import ContentChannelName


class _AgentDependencies(BaseModel):
    brand: Brand
    channel: ContentChannelName


class _AgentOutputFromUserMedia(BaseModel):
    caption: str

    model_config = ConfigDict(from_attributes=True)


class FromUserMediaTextWithSingleImageContentGenerationJobStrategy(
    base_strategy.BaseTextWithSingleImageContentGenerationJobStrategy
):
    def __init__(
        self,
        session_factory: DbSessionFactory = Depends(),
        prompt_service: PromptService = Depends(),
    ):
        self.session_factory = session_factory
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
        brand: Brand = await brand_service.get(self.session_factory, job.brand_id)
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
                (
                    "User input type is not valid for text with single image "
                    "content generation job."
                ),
            )
        return job.user_input
