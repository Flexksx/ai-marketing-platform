from datetime import UTC

import public
from fastapi import Depends
from pydantic import BaseModel, ConfigDict
from pydantic_ai import Agent, ImageUrl, RunContext, format_as_xml

import src.brands.service as brand_service
import src.content_channel.service as content_channel_service
import src.content_plan_item.service as content_plan_item_service
from lib.ai_agents.schema import PydanticAiModel
from lib.db.session_factory import DbSessionFactory
from lib.prompts import PromptService, PromptTemplateName
from src.campaign_generation.generation.content_plan.model import (
    AgentGeneratedPostingPlanItem,
    AgentGeneratedPostingPlanResult,
)
from src.campaign_generation.generation.errors import (
    CampaignGenerationJobGenerationFailureException,
)
from webapp_api_contract.brands import Brand
from webapp_api_contract.campaign_generation import (
    CampaignGenerationJob,
    CampaignGenerationJobResult,
    CampaignGenerationJobResultElementNotFoundException,
    CampaignGenerationJobResultNotFoundException,
    ContentBriefCampaignGenerationJobResult,
    UserMediaOnlyCampaignGenerationJobUserInput,
)
from webapp_api_contract.content_plan_items import ContentPlanItemCreateRequest
from webapp_api_contract.shared import ContentChannel


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
        session_factory: DbSessionFactory = Depends(),
        prompt_service: PromptService = Depends(),
    ):
        self.session_factory = session_factory
        self.prompt_service = prompt_service
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
        brand = await brand_service.get(self.session_factory, job.brand_id)
        user_input = self.__get_user_input_or_raise(job)
        content_brief = self.__get_campaign_description_result(job)
        available_channels = content_channel_service.search()

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
        existing_items = await content_plan_item_service.search(
            self.session_factory,
            job.id,
        )
        if len(existing_items) == 0:
            create_requests = [
                ContentPlanItemCreateRequest(
                    job_id=job.id,
                    description=item.description,
                    channel=item.channel,
                    content_type=item.content_type,
                    content_format=item.content_format,
                    image_urls=[item.image_url],
                    scheduled_at=item.scheduled_at.astimezone(UTC).replace(tzinfo=None),
                )
                for item in user_images_only_content_plan_generation_result.plan_items
            ]
            existing_items = await content_plan_item_service.create_many(
                self.session_factory,
                job.id,
                create_requests,
            )

        current_result.content_plan_items = existing_items
        return current_result
