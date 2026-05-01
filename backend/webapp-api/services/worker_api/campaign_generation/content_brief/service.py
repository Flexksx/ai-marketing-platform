import public
from fastapi import Depends
from pydantic import BaseModel, Field
from pydantic_ai import Agent, ImageUrl, RunContext

from aimarketing.domain.brand import Brand, BrandService
from aimarketing.domain.brand_settings import ContentPillarBusinessGoal
from aimarketing.domain.campaign_generation import CampaignGenerationJobService
from aimarketing.domain.campaign_generation.model import (
    CampaignGenerationJobResult,
    ContentBriefCampaignGenerationJobResult,
)
from aimarketing.domain.content_channel import (
    ContentChannel,
    ContentChannelName,
    ContentChannelService,
)
from aimarketing.lib.ai_agents import PydanticAiModel
from aimarketing.lib.prompts import PromptService, PromptTemplateName


@public.add
class CampaignContentBriefAgentResult(BaseModel):
    name: str
    description: str
    goal: ContentPillarBusinessGoal
    target_audience_ids: list[str] = Field(
        default_factory=list, description="Only the IDs of the target audience"
    )
    content_pillar_ids: list[str] = Field(
        default_factory=list, description="Only the IDs of the content pillars"
    )
    channels: list[ContentChannelName] = Field(default_factory=list)


@public.add
class CampaignContentBriefAgentDependencies(BaseModel):
    brand: Brand
    content_channels: list[ContentChannel]
    description_prompt_name: PromptTemplateName


@public.add
class CampaignContentBriefGenerator:
    def __init__(
        self,
        prompt_service: PromptService = Depends(),
        brand_service: BrandService = Depends(),
        campaign_generation_job_service: CampaignGenerationJobService = Depends(),
        content_channel_service: ContentChannelService = Depends(),
    ):
        self.prompt_service = prompt_service
        self.brand_service = brand_service
        self.content_channel_service = content_channel_service
        self.campaign_generation_job_service = campaign_generation_job_service

        self.__agent = Agent(
            model=PydanticAiModel.GEMINI_FLASH_LITE_LATEST,
            deps_type=CampaignContentBriefAgentDependencies,
            output_type=CampaignContentBriefAgentResult,
        )

        @self.__agent.system_prompt
        def __set_system_prompt(
            context: RunContext[CampaignContentBriefAgentDependencies],
        ):
            return self.prompt_service.render(
                context.deps.description_prompt_name, context.deps.model_dump()
            )

    async def generate(
        self,
        job_id: str,
        brand_id: str,
        user_prompt: str,
        image_urls: list[ImageUrl],
        description_prompt_name: PromptTemplateName,
    ) -> CampaignGenerationJobResult:
        brand = await self.brand_service.get(brand_id)
        content_channels = self.content_channel_service.search()
        deps = CampaignContentBriefAgentDependencies(
            brand=brand,
            content_channels=content_channels,
            description_prompt_name=description_prompt_name,
        )

        run_result = await self.__agent.run(
            user_prompt=[user_prompt, *image_urls],
            deps=deps,
        )
        brief_result: CampaignContentBriefAgentResult = run_result.output  # ty:ignore[invalid-assignment]

        return await self.__merge_campaign_result(job_id, brief_result)

    async def __merge_campaign_result(
        self,
        job_id: str,
        agent_result: CampaignContentBriefAgentResult,
    ) -> CampaignGenerationJobResult:
        job = await self.campaign_generation_job_service.get(job_id)
        current_result = job.get_result()
        if current_result is None:
            current_result = CampaignGenerationJobResult()
        current_result.content_brief = ContentBriefCampaignGenerationJobResult(
            name=agent_result.name,
            goal=agent_result.goal,
            description=agent_result.description,
            target_audience_ids=agent_result.target_audience_ids,
            content_pillar_ids=agent_result.content_pillar_ids,
            channels=agent_result.channels,
            start_date=job.user_input.start_date,
            end_date=job.user_input.end_date,
        )
        return current_result
