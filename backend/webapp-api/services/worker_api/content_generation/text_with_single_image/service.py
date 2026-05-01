import public
from fastapi import Depends
from pydantic import BaseModel, ConfigDict

from services.worker_api.content_generation.shared import (
    BaseContentGenerationJobRunner,
)
from services.worker_api.content_generation.text_with_single_image.ai_generated_image import (
    AIGeneratedImageTextWithSingleImageContentGenerationJobStrategy,
)
from services.worker_api.content_generation.text_with_single_image.base_strategy import (
    BaseTextWithSingleImageContentGenerationJobStrategy,
)
from services.worker_api.content_generation.text_with_single_image.from_user_media import (
    FromUserMediaTextWithSingleImageContentGenerationJobStrategy,
)
from services.worker_api.content_generation.text_with_single_image.product_lifestyle import (
    ProductLifestyleTextWithSingleImageContentGenerationJobStrategy,
)
from aimarketing.domain.brand import Brand
from aimarketing.domain.content_channel import ContentChannelName
from aimarketing.domain.content_generation_job import (
    AiGeneratedTextWithSingleImageContentGenerationJobUserInput,
    ContentGenerationJob,
    ContentGenerationJobInvalidUserInputException,
    ContentGenerationJobUnsupportedWorkflowTypeException,
    ContentGenerationJobWorkflowType,
    FromUserMediaTextWithSingleImageContentGenerationJobUserInput,
    ProductLifestyleTextWithSingleImageContentGenerationJobUserInput,
    TextWithSingleImageContentGenerationJobResult,
)
from aimarketing.domain.content_generation_job.service import ContentGenerationJobService


class _AgentOutputFromUserMedia(BaseModel):
    caption: str

    model_config = ConfigDict(from_attributes=True)


class _CopywritingAgentTemplateDependencies(BaseModel):
    brand: Brand
    channel: ContentChannelName


@public.add
class TextWithSingleImageContentGenerationJobRunner(BaseContentGenerationJobRunner):
    def __init__(
        self,
        content_generation_job_service: ContentGenerationJobService = Depends(),
        from_user_media_strategy: (
            FromUserMediaTextWithSingleImageContentGenerationJobStrategy
        ) = Depends(),
        ai_generated_image_strategy: (
            AIGeneratedImageTextWithSingleImageContentGenerationJobStrategy
        ) = Depends(),
        product_lifestyle_strategy: (
            ProductLifestyleTextWithSingleImageContentGenerationJobStrategy
        ) = Depends(),
    ):
        super().__init__(content_generation_job_service)
        self.from_user_media_strategy = from_user_media_strategy
        self.ai_generated_image_strategy = ai_generated_image_strategy
        self.product_lifestyle_strategy = product_lifestyle_strategy

    async def generate_result(
        self, job: ContentGenerationJob
    ) -> TextWithSingleImageContentGenerationJobResult:
        workflow_type = self.__get_validated_workflow_type_or_raise(job)
        workflow_type_strategy_map = {
            ContentGenerationJobWorkflowType.TEXT_WITH_SINGLE_IMAGE_FROM_USER_MEDIA: (
                self.from_user_media_strategy
            ),
            ContentGenerationJobWorkflowType.TEXT_WITH_SINGLE_IMAGE_AI_GENERATED: (
                self.ai_generated_image_strategy
            ),
            ContentGenerationJobWorkflowType.TEXT_WITH_SINGLE_IMAGE_PRODUCT_LIFESTYLE: (
                self.product_lifestyle_strategy
            ),
        }
        strategy: BaseTextWithSingleImageContentGenerationJobStrategy | None = (
            workflow_type_strategy_map.get(workflow_type)
        )
        if strategy is None:
            raise ContentGenerationJobUnsupportedWorkflowTypeException(
                job.id,
                workflow_type,
            )
        return await strategy.generate(job)

    def __get_validated_workflow_type_or_raise(
        self, job: ContentGenerationJob
    ) -> ContentGenerationJobWorkflowType:
        user_input = job.user_input
        workflow_type = user_input.workflow_type

        validation_map = {
            ContentGenerationJobWorkflowType.TEXT_WITH_SINGLE_IMAGE_FROM_USER_MEDIA: (
                FromUserMediaTextWithSingleImageContentGenerationJobUserInput,
                "Image URL is required for USER_MEDIA workflow type.",
            ),
            ContentGenerationJobWorkflowType.TEXT_WITH_SINGLE_IMAGE_AI_GENERATED: (
                AiGeneratedTextWithSingleImageContentGenerationJobUserInput,
                "User input type is not valid for AI-generated image workflow type.",
            ),
            ContentGenerationJobWorkflowType.TEXT_WITH_SINGLE_IMAGE_PRODUCT_LIFESTYLE: (
                ProductLifestyleTextWithSingleImageContentGenerationJobUserInput,
                "Product image URL is required for PRODUCT_LIFESTYLE workflow type.",
            ),
        }

        if workflow_type in validation_map:
            expected_class, error_message = validation_map[workflow_type]
            if not isinstance(user_input, expected_class):
                raise ContentGenerationJobInvalidUserInputException(
                    job.id, error_message
                )
        return workflow_type
