from fastapi import Depends
from pydantic import BaseModel

from src.content_generation_job.generation.text_with_single_image.base_strategy import (
    BaseTextWithSingleImageContentGenerationJobStrategy,
)
from src.shared import (
    TextWithSingleImageContent,
    TextWithSingleImageContentGenerator,
)
from webapp_api_contract.brands import Brand
from webapp_api_contract.content import TextWithSingleImageContentData
from webapp_api_contract.shared import ContentChannelName
from webapp_api_contract.content_generation import (
    AiGeneratedTextWithSingleImageContentGenerationJobUserInput,
    ContentGenerationJob,
    ContentGenerationJobInvalidUserInputException,
    TextWithSingleImageContentGenerationJobResult,
)
from lib.prompts import PromptTemplateName


class _AgentDependencies(BaseModel):
    brand: Brand
    channel: ContentChannelName


class AIGeneratedImageTextWithSingleImageContentGenerationJobStrategy(
    BaseTextWithSingleImageContentGenerationJobStrategy
):
    def __init__(
        self,
        text_with_single_image_content_generation_service: TextWithSingleImageContentGenerator = Depends(),
    ):
        self.text_with_single_image_content_generation_service = (
            text_with_single_image_content_generation_service
        )

    async def generate(
        self, job: ContentGenerationJob
    ) -> TextWithSingleImageContentGenerationJobResult:
        user_input = self.__get_ai_generated_user_input_or_raise(job)

        result: TextWithSingleImageContent = await self.text_with_single_image_content_generation_service.generate_full(
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

    def __get_ai_generated_user_input_or_raise(
        self, job: ContentGenerationJob
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
