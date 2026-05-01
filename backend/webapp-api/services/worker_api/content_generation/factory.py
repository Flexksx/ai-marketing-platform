import public
from fastapi import Depends

from services.worker_api.content_generation.shared.service import (
    BaseContentGenerationJobRunner,
)
from services.worker_api.content_generation.text_with_single_image.service import (
    TextWithSingleImageContentGenerationJobRunner,
)
from aimarketing.domain.content_generation_job import (
    ContentGenerationJob,
    ContentGenerationJobInvalidUserInputException,
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
