from typing import Literal

import public
from pydantic import AliasChoices, ConfigDict, Field

from vozai.domain.content import TextWithSingleImageContentData
from vozai.domain.content_generation_job.base import (
    BaseContentGenerationJobResult,
    BaseContentGenerationJobUserInput,
)
from vozai.domain.content_generation_job.enum import ContentGenerationJobWorkflowType


@public.add
class FromUserMediaTextWithSingleImageContentGenerationJobUserInput(
    BaseContentGenerationJobUserInput
):
    image_url: str
    workflow_type: Literal[
        ContentGenerationJobWorkflowType.TEXT_WITH_SINGLE_IMAGE_FROM_USER_MEDIA
    ] = ContentGenerationJobWorkflowType.TEXT_WITH_SINGLE_IMAGE_FROM_USER_MEDIA

    model_config = ConfigDict(from_attributes=True)


@public.add
class AiGeneratedTextWithSingleImageContentGenerationJobUserInput(
    BaseContentGenerationJobUserInput
):
    workflow_type: Literal[
        ContentGenerationJobWorkflowType.TEXT_WITH_SINGLE_IMAGE_AI_GENERATED
    ] = ContentGenerationJobWorkflowType.TEXT_WITH_SINGLE_IMAGE_AI_GENERATED

    model_config = ConfigDict(from_attributes=True)


@public.add
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


@public.add
class TextWithSingleImageContentGenerationJobResult(BaseContentGenerationJobResult):
    data: TextWithSingleImageContentData

    model_config = ConfigDict(from_attributes=True)
