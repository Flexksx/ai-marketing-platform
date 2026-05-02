from datetime import datetime
from typing import Annotated, Literal

from pydantic import AliasChoices, BaseModel, ConfigDict, Field

from webapp_api_contract.content import (
    TextOnlyContentData,
    TextWithSingleImageContentData,
)
from webapp_api_contract.shared import (
    ContentChannelName,
    ContentFormat,
    ContentGenerationJobWorkflowType,
    JobStatus,
)


class BaseContentGenerationJobUserInput(BaseModel):
    prompt: str = Field(...)
    channel: ContentChannelName = Field(...)
    scheduled_at: datetime = Field(...)

    model_config = ConfigDict(from_attributes=True)


class BaseContentGenerationJobResult(BaseModel):
    channel: ContentChannelName
    scheduled_at: datetime

    model_config = ConfigDict(from_attributes=True)


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


class TextWithSingleImageContentGenerationJobResult(BaseContentGenerationJobResult):
    data: TextWithSingleImageContentData

    model_config = ConfigDict(from_attributes=True)


class FromUserMediaTextWithSingleImageContentGenerationJobUserInput(
    BaseContentGenerationJobUserInput
):
    image_url: str
    workflow_type: Literal[
        ContentGenerationJobWorkflowType.TEXT_WITH_SINGLE_IMAGE_FROM_USER_MEDIA
    ] = ContentGenerationJobWorkflowType.TEXT_WITH_SINGLE_IMAGE_FROM_USER_MEDIA

    model_config = ConfigDict(from_attributes=True)


class AiGeneratedTextWithSingleImageContentGenerationJobUserInput(
    BaseContentGenerationJobUserInput
):
    workflow_type: Literal[
        ContentGenerationJobWorkflowType.TEXT_WITH_SINGLE_IMAGE_AI_GENERATED
    ] = ContentGenerationJobWorkflowType.TEXT_WITH_SINGLE_IMAGE_AI_GENERATED

    model_config = ConfigDict(from_attributes=True)


class ProductLifestyleTextWithSingleImageContentGenerationJobUserInput(
    BaseContentGenerationJobUserInput
):
    image_url: str = Field(
        validation_alias=AliasChoices("image_url", "product_image_url")
    )
    workflow_type: Literal[
        ContentGenerationJobWorkflowType.TEXT_WITH_SINGLE_IMAGE_PRODUCT_LIFESTYLE
    ] = ContentGenerationJobWorkflowType.TEXT_WITH_SINGLE_IMAGE_PRODUCT_LIFESTYLE

    model_config = ConfigDict(from_attributes=True)


ContentGenerationJobUserInput = Annotated[
    TextOnlyContentGenerationJobUserInput
    | FromUserMediaTextWithSingleImageContentGenerationJobUserInput
    | AiGeneratedTextWithSingleImageContentGenerationJobUserInput
    | ProductLifestyleTextWithSingleImageContentGenerationJobUserInput,
    Field(discriminator="workflow_type"),
]

ContentGenerationJobResult = (
    TextOnlyContentGenerationJobResult | TextWithSingleImageContentGenerationJobResult
)


class ContentGenerationJob(BaseModel):
    id: str
    brand_id: str
    status: JobStatus
    content_format: ContentFormat
    user_input: ContentGenerationJobUserInput
    result: ContentGenerationJobResult | None = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
