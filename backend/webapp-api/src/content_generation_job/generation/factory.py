import public
from fastapi import Depends

from src.content_generation_job.generation.shared.service import (
    BaseContentGenerationJobRunner,
)
from src.content_generation_job.generation.text_with_single_image.service import (
    TextWithSingleImageContentGenerationJobRunner,
)
from src.content_generation_job.errors import ContentGenerationJobInvalidUserInputException
from webapp_api_contract.content_generation import (
    ContentGenerationJob,
    ContentGenerationJobWorkflowType,
)


@public.add
class ContentGenerationJobRunnerFactory:
    def __init__(
        self,
        text_with_single_image_runner: TextWithSingleImageContentGenerationJobRunner = Depends(),
    ):
        self.text_with_single_image_runner = text_with_single_image_runner

    def get_runner(self, job: ContentGenerationJob) -> BaseContentGenerationJobRunner:
        workflow_type_strategy_map = {
            ContentGenerationJobWorkflowType.TEXT_WITH_SINGLE_IMAGE_FROM_USER_MEDIA: self.text_with_single_image_runner,
            ContentGenerationJobWorkflowType.TEXT_WITH_SINGLE_IMAGE_AI_GENERATED: self.text_with_single_image_runner,
            ContentGenerationJobWorkflowType.TEXT_WITH_SINGLE_IMAGE_PRODUCT_LIFESTYLE: self.text_with_single_image_runner,
        }
        runner = workflow_type_strategy_map.get(job.user_input.workflow_type)
        if not runner:
            raise ContentGenerationJobInvalidUserInputException(
                job.id,
                "Requested workflow type is not supported.",
            )
        return runner
