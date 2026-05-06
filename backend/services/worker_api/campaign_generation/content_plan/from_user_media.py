from datetime import UTC

import public
from fastapi import Depends
from pydantic import BaseModel, ConfigDict
from pydantic_ai import Agent, ImageUrl, RunContext, format_as_xml

from services.worker_api.campaign_generation.content_plan.model import (
    AgentGeneratedPostingPlanItem,
    AgentGeneratedPostingPlanResult,
)
from services.worker_api.campaign_generation.errors import (
    CampaignGenerationJobGenerationFailureException,
)
from vozai.domain.brand import Brand, BrandService
from vozai.domain.campaign_generation import (
    CampaignGenerationJob,
    CampaignGenerationJobResultElementNotFoundException,
    CampaignGenerationJobResultNotFoundException,
    ContentBriefCampaignGenerationJobResult,
)
from vozai.domain.campaign_generation.model import CampaignGenerationJobResult
from vozai.domain.campaign_generation.user_media_only.model import (
    UserMediaOnlyCampaignGenerationJobUserInput,
)
from vozai.domain.content_channel import ContentChannel, ContentChannelService
from vozai.domain.content_plan_item.schema import ContentPlanItemCreateRequest
from vozai.domain.content_plan_item.service import ContentPlanItemService
from vozai.lib.ai_agents.schema import PydanticAiModel
from vozai.lib.prompts import PromptService, PromptTemplateName


class UserImagesOnlyContentPlanGenerationDependencies(BaseModel):
    brand: Brand
    user_input: UserMediaOnlyCampaignGenerationJobUserInput
    available_channels: list[ContentChannel]


class UserImagesOnlyContentPlanGenerationItem(AgentGeneratedPostingPlanItem):
    image_url: str


class UserImagesOnlyContentPlanGenerationOutput(AgentGeneratedPostingPlanResult):
    plan_items: list[UserImagesOnlyContentPlanGenerationItem]
    model_config = ConfigDict(from_attributes=True)


@public.add
class UserMediaContentPlanGenerator:
    def __init__(
        self,
        brand_service: BrandService = Depends(),
        prompt_service: PromptService = Depends(),
        content_channel_service: ContentChannelService = Depends(),
        content_plan_item_service: ContentPlanItemService = Depends(),
    ):
        self.brand_service = brand_service
        self.prompt_service = prompt_service
        self.content_channel_service = content_channel_service
        self.content_plan_item_service = content_plan_item_service
        self.__agent = Agent(
            model=PydanticAiModel.GEMINI_FLASH_LITE_LATEST,
            deps_type=UserImagesOnlyContentPlanGenerationDependencies,
            output_type=UserImagesOnlyContentPlanGenerationOutput,
        )

        @self.__agent.system_prompt
        def __set_system_prompt(
            context: RunContext[UserImagesOnlyContentPlanGenerationDependencies],
        ):
            return self.prompt_service.render(
                PromptTemplateName.CAMPAIGN_GENERATION_CONTENT_PLAN_STEP_FROM_USER_MEDIA,
                context.deps.model_dump(),
            )

    async def generate(self, job: CampaignGenerationJob) -> CampaignGenerationJobResult:
        brand = await self.brand_service.get(job.brand_id)
        user_input = self.__get_user_input_or_raise(job)
        content_brief = self.__get_campaign_description_result(job)
        available_channels = self.content_channel_service.search()

        deps = UserImagesOnlyContentPlanGenerationDependencies(
            brand=brand,
            user_input=user_input,
            available_channels=available_channels,
        )

        ai_response = await self.__agent.run(
            user_prompt=[
                format_as_xml([user_input, content_brief]),
                *[ImageUrl(url) for url in user_input.image_urls],
            ],
            deps=deps,
        )
        posting_plan_result: UserImagesOnlyContentPlanGenerationOutput = (
            ai_response.output
        )  # ty:ignore[invalid-assignment]
        if not posting_plan_result:
            raise CampaignGenerationJobGenerationFailureException(
                job.id,
                "No output from agent for content plan generation",
            )
        return await self.__merge_campaign_result(job, posting_plan_result)

    def __get_user_input_or_raise(
        self, job: CampaignGenerationJob
    ) -> UserMediaOnlyCampaignGenerationJobUserInput:
        if not isinstance(job.user_input, UserMediaOnlyCampaignGenerationJobUserInput):
            raise ValueError(f"User input is not a valid user input for job {job.id}")
        return job.user_input

    def __get_campaign_description_result(
        self, job: CampaignGenerationJob
    ) -> ContentBriefCampaignGenerationJobResult:
        description_result = job.get_description_result()
        if not description_result:
            raise CampaignGenerationJobResultElementNotFoundException(
                job.id, "description_result"
            )
        return description_result

    async def __merge_campaign_result(
        self,
        job: CampaignGenerationJob,
        user_images_only_content_plan_generation_result: (
            UserImagesOnlyContentPlanGenerationOutput
        ),
    ) -> CampaignGenerationJobResult:
        current_result = job.get_result()
        if not current_result:
            raise CampaignGenerationJobResultNotFoundException(job.id)
        existing_items = await self.content_plan_item_service.search(job.id)
        if len(existing_items) == 0:
            create_requests = [
                ContentPlanItemCreateRequest(
                    job_id=job.id,
                    description=item.description,
                    channel=item.channel,
                    content_type=item.content_type,
                    content_format=item.content_format,
                    image_urls=[item.image_url],
                    scheduled_at=item.scheduled_at.astimezone(UTC).replace(
                        tzinfo=None
                    ),
                )
                for item in user_images_only_content_plan_generation_result.plan_items
            ]
            existing_items = await self.content_plan_item_service.create_many(
                job.id, create_requests
            )

        current_result.content_plan_items = existing_items
        return current_result
