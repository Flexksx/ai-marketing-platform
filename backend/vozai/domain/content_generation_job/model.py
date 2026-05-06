from datetime import datetime
from typing import Annotated

import public
from pydantic import BaseModel, ConfigDict, Field

from vozai.domain.content_channel import ContentFormat
from vozai.domain.content_generation_job.content_type.text_only import (
    TextOnlyContentGenerationJobResult,
    TextOnlyContentGenerationJobUserInput,
)
from vozai.domain.content_generation_job.content_type.text_with_single_image import (
    AiGeneratedTextWithSingleImageContentGenerationJobUserInput,
    FromUserMediaTextWithSingleImageContentGenerationJobUserInput,
    ProductLifestyleTextWithSingleImageContentGenerationJobUserInput,
    TextWithSingleImageContentGenerationJobResult,
)
from vozai.lib.job.model import JobStatus


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


@public.add
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
