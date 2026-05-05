from pydantic import BaseModel, Field
from pydantic_ai import Agent, ImageUrl, RunContext

import src.brand.service as brand_service
import src.campaign_generation.service as campaign_generation_job_service
import src.content_channel.service as content_channel_service
from lib.ai_agents import PydanticAiModel
from lib.db.session_factory import DbSessionFactory
from lib.prompts import PromptService, PromptTemplateName
from src.brand.model import Brand, ContentPillarBusinessGoal
from src.campaign_generation.model import (
    CampaignGenerationJob,
    CampaignGenerationJobResult,
    ContentBriefCampaignGenerationJobResult,
)
from src.shared.model import ContentChannel, ContentChannelName


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


class _AgentDependencies(BaseModel):
    brand: Brand
    content_channels: list[ContentChannel]
    description_prompt_name: PromptTemplateName


_prompt_service = PromptService()

_agent: Agent[_AgentDependencies, CampaignContentBriefAgentResult] = Agent(
    model=PydanticAiModel.GEMINI_FLASH_LITE_LATEST,
    deps_type=_AgentDependencies,
    output_type=CampaignContentBriefAgentResult,
)


@_agent.system_prompt
def _get_system_prompt(context: RunContext[_AgentDependencies]) -> str:
    return _prompt_service.render(
        context.deps.description_prompt_name, context.deps.model_dump()
    )


async def generate_content_brief(
    job: CampaignGenerationJob,
    session_factory: DbSessionFactory,
    image_urls: list[ImageUrl] | None = None,
) -> CampaignGenerationJobResult:
    brand = await brand_service.get(session_factory, job.brand_id)
    content_channels = content_channel_service.search()
    deps = _AgentDependencies(
        brand=brand,
        content_channels=content_channels,
        description_prompt_name=PromptTemplateName.CAMPAIGN_GENERATION_DESCRIPTION_STEP,
    )
    run_result = await _agent.run(
        user_prompt=[job.user_input.prompt, *(image_urls or [])],
        deps=deps,
    )
    brief_result: CampaignContentBriefAgentResult = run_result.output
    return await _merge_campaign_result(session_factory, job.id, brief_result)


async def _merge_campaign_result(
    session_factory: DbSessionFactory,
    job_id: str,
    agent_result: CampaignContentBriefAgentResult,
) -> CampaignGenerationJobResult:
    job = await campaign_generation_job_service.get(session_factory, job_id)
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
