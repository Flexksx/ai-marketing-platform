from typing import Literal

from pydantic import ConfigDict, Field

from webapp_api_contract.content import TextOnlyContentData
from webapp_api_contract.content_generation import (
    BaseContentGenerationJobResult,
    BaseContentGenerationJobUserInput,
)
from webapp_api_contract.shared import (
    ContentChannelName,
    ContentGenerationJobWorkflowType,
)


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
