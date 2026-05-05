from pydantic import BaseModel, Field
from pydantic_ai import Agent, ImageUrl, RunContext

import src.brand.service as brand_service
import src.campaign_generation.service as campaign_generation_job_service
import src.content_channel.service as content_channel_service
from lib import prompts
from lib.ai_agents import PydanticAiModel
from lib.model import ContentChannelName
from lib.prompts import PromptTemplateName
from src.brand.model import Brand, ContentPillarBusinessGoal
from src.campaign_generation.model import (
    CampaignGenerationJob,
    CampaignGenerationJobResult,
    ContentBriefCampaignGenerationJobResult,
)
from src.content_channel.model import ContentChannel


class _CampaignContentBriefAgentResult(BaseModel):
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


class _AgentDependencies(BaseModel):
    brand: Brand
    content_channels: list[ContentChannel]


_agent: Agent[_AgentDependencies, _CampaignContentBriefAgentResult] = Agent(  # ty:ignore[invalid-assignment]
    model=PydanticAiModel.GEMINI_FLASH_LITE_LATEST,
    deps_type=_AgentDependencies,
    output_type=_CampaignContentBriefAgentResult,
)


@_agent.system_prompt
def _get_system_prompt(context: RunContext[_AgentDependencies]) -> str:
    return prompts.render(
        PromptTemplateName.CAMPAIGN_GENERATION_DESCRIPTION_STEP,
        context.deps.model_dump(),
    )


async def generate_content_brief(
    job: CampaignGenerationJob,
    image_urls: list[ImageUrl] | None = None,
) -> CampaignGenerationJobResult:
    brand = await brand_service.get(job.brand_id)
    content_channels = content_channel_service.search()
    deps = _AgentDependencies(brand=brand, content_channels=content_channels)
    run_result = await _agent.run(
        user_prompt=[job.user_input.prompt, *(image_urls or [])],
        deps=deps,
    )
    return await _merge_campaign_result(job.id, run_result.output)


async def _merge_campaign_result(
    job_id: str,
    agent_result: _CampaignContentBriefAgentResult,
) -> CampaignGenerationJobResult:
    job = await campaign_generation_job_service.get(job_id)
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
