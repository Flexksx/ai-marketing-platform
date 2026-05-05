from pydantic import BaseModel, ConfigDict
from pydantic_ai import Agent, ImageUrl, RunContext

import src.brand.service as brand_service
from lib.ai_agents.schema import PydanticAiModel
from lib.db.session_factory import DbSessionFactory
from lib.prompts import PromptService, PromptTemplateName
from src.brand.model import Brand
from src.content.model import TextWithSingleImageContentData
from src.content_generation_job.errors import (
    ContentGenerationJobInvalidUserInputException,
)
from src.content_generation_job.model import (
    ContentGenerationJob,
    FromUserMediaTextWithSingleImageContentGenerationJobUserInput,
    TextWithSingleImageContentGenerationJobResult,
)
from src.shared.model import ContentChannelName


class _AgentDependencies(BaseModel):
    brand: Brand
    channel: ContentChannelName


class _AgentOutput(BaseModel):
    caption: str

    model_config = ConfigDict(from_attributes=True)


_prompt_service = PromptService()

_agent: Agent[_AgentDependencies, _AgentOutput] = Agent(
    model=PydanticAiModel.GEMINI_FLASH_LATEST,
    deps_type=_AgentDependencies,
    output_type=_AgentOutput,
)


@_agent.system_prompt
def _get_system_prompt(context: RunContext[_AgentDependencies]) -> str:
    return _prompt_service.render(
        PromptTemplateName.TEXT_WITH_SINGLE_IMAGE_CAPTION,
        context.deps.model_dump(),
    )


async def generate_result(
    job: ContentGenerationJob,
    session_factory: DbSessionFactory,
) -> TextWithSingleImageContentGenerationJobResult:
    user_input = _get_user_input_or_raise(job)
    brand: Brand = await brand_service.get(session_factory, job.brand_id)
    agent_run = await _agent.run(
        user_prompt=[
            user_input.prompt,
            ImageUrl(url=user_input.image_url),
        ],
        deps=_AgentDependencies(brand=brand, channel=user_input.channel),
    )
    result: _AgentOutput = agent_run.output
    return TextWithSingleImageContentGenerationJobResult(
        data=TextWithSingleImageContentData(
            caption=result.caption,
            image_url=user_input.image_url,
        ),
        channel=user_input.channel,
        scheduled_at=user_input.scheduled_at,
    )


def _get_user_input_or_raise(
    job: ContentGenerationJob,
) -> FromUserMediaTextWithSingleImageContentGenerationJobUserInput:
    if not isinstance(
        job.user_input,
        FromUserMediaTextWithSingleImageContentGenerationJobUserInput,
    ):
        raise ContentGenerationJobInvalidUserInputException(
            job.id,
            "User input type is not valid for from-user-media content generation job.",
        )
    return job.user_input
