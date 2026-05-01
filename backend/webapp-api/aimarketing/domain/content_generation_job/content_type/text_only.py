from typing import Literal

from pydantic import ConfigDict, Field

from aimarketing.domain.content import TextOnlyContentData
from aimarketing.domain.content_channel.model import ContentChannelName
from aimarketing.domain.content_generation_job.base import (
    BaseContentGenerationJobResult,
    BaseContentGenerationJobUserInput,
)
from aimarketing.domain.content_generation_job.enum import ContentGenerationJobWorkflowType


class TextOnlyContentGenerationJobResult(BaseContentGenerationJobResult):
    data: TextOnlyContentData

    model_config = ConfigDict(from_attributes=True)


class TextOnlyContentGenerationJobUserInput(BaseContentGenerationJobUserInput):
    prompt: str = Field(...)
    channels: list[ContentChannelName] = Field(...)
    workflow_type: Literal[ContentGenerationJobWorkflowType.TEXT_ONLY] = (
        ContentGenerationJobWorkflowType.TEXT_ONLY
    )

    model_config = ConfigDict(from_attributes=True)
