import logging
from datetime import UTC

import public
from fastapi import Depends
from pydantic import BaseModel
from pydantic_ai import Agent, RunContext, format_as_xml

from services.worker_api.campaign_generation.content_plan.model import (
    AgentGeneratedPostingPlanResult,
)
from services.worker_api.campaign_generation.errors import (
    CampaignGenerationJobGenerationFailureException,
)
from aimarketing.domain.brand import Brand, BrandService
from aimarketing.domain.campaign_generation import (
    CampaignGenerationJob,
    CampaignGenerationJobResultNotFoundException,
    CampaignGenerationJobService,
)
from aimarketing.domain.campaign_generation.model import CampaignGenerationJobResult
from aimarketing.domain.content_channel import ContentChannel, ContentChannelService
from aimarketing.domain.content_plan_item.schema import ContentPlanItemCreateRequest
from aimarketing.domain.content_plan_item.service import ContentPlanItemService
from aimarketing.lib.ai_agents import PydanticAiModel
from aimarketing.lib.prompts import PromptService, PromptTemplateName


logger = logging.getLogger(__name__)


class ContentPlanAgentDependencies(BaseModel):
    brand: Brand
    available_channels: list[ContentChannel]
    prompt_template_name: PromptTemplateName


@public.add
class AIGeneratedContentPlanGenerator:
    def __init__(
        self,
        prompt_service: PromptService = Depends(),
        campaign_generation_job_service: CampaignGenerationJobService = Depends(),
        content_channel_service: ContentChannelService = Depends(),
        brand_service: BrandService = Depends(),
        content_plan_item_service: ContentPlanItemService = Depends(),
    ):
        self.prompt_service = prompt_service
        self.brand_service = brand_service
        self.campaign_generation_job_service = campaign_generation_job_service
        self.content_channel_service = content_channel_service
        self.content_plan_item_service = content_plan_item_service

        self.__agent = Agent(
            model=PydanticAiModel.GEMINI_FLASH_LATEST,
            deps_type=ContentPlanAgentDependencies,
            output_type=AgentGeneratedPostingPlanResult,
        )

        @self.__agent.system_prompt
        def __set_system_prompt(
            context: RunContext[ContentPlanAgentDependencies],
        ):
            return self.prompt_service.render(
                context.deps.prompt_template_name,
                context.deps.model_dump(),
            )

    async def generate(
        self, job: CampaignGenerationJob, prompt_template_name: PromptTemplateName
    ) -> CampaignGenerationJobResult:
        try:
            user_input = job.user_input
            brand = await self.brand_service.get(job.brand_id)
            campaign_description_result = (
                job.result.content_brief if job.result else None
            )
            if campaign_description_result is None:
                raise ValueError("Campaign description result is missing")

            available_channels = self.content_channel_service.search()

            dependencies = ContentPlanAgentDependencies(
                brand=brand,
                prompt_template_name=prompt_template_name,
                available_channels=available_channels,
            )
            result = await self.__agent.run(
                user_prompt=[
                    format_as_xml([user_input.prompt, campaign_description_result])
                ],
                deps=dependencies,
            )
            content_plan: AgentGeneratedPostingPlanResult = result.output  # ty:ignore[invalid-assignment]
            return await self.merge_to_campaign_generation_job_result(
                job, content_plan
            )

        except Exception as e:
            logger.error(
                f"Failed to generate posting plan for job {job.id}: {e}",
                exc_info=True,
                extra={"job_id": job.id},
            )
            raise CampaignGenerationJobGenerationFailureException(
                job.id, f"Failed to generate content plan: {e}"
            ) from e

    async def merge_to_campaign_generation_job_result(
        self,
        job: CampaignGenerationJob,
        agent_posting_plan_result: AgentGeneratedPostingPlanResult,
    ) -> CampaignGenerationJobResult:
        current_result = job.get_result()
        if not current_result:
            raise CampaignGenerationJobResultNotFoundException(job.id)
        existing_items = await self.content_plan_item_service.search(job.id)
        if len(existing_items) == 0:
            create_requests = [
                ContentPlanItemCreateRequest(
                    job_id=job.id,
                    description=agent_posting_plan_item.description,
                    channel=agent_posting_plan_item.channel,
                    content_type=agent_posting_plan_item.content_type,
                    content_format=agent_posting_plan_item.content_format,
                    image_urls=[],
                    scheduled_at=agent_posting_plan_item.scheduled_at.astimezone(
                        UTC
                    ).replace(tzinfo=None),
                )
                for agent_posting_plan_item in agent_posting_plan_result.plan_items
            ]
            existing_items = await self.content_plan_item_service.create_many(
                job.id, create_requests
            )

        current_result.content_plan_items = existing_items
        return current_result
