from datetime import datetime
from typing import Annotated

import public
from pydantic import BaseModel, ConfigDict, Field

from webapp_api_contract.shared import ContentFormat
from webapp_api_contract.content_generation import (
    TextOnlyContentGenerationJobResult,
    TextOnlyContentGenerationJobUserInput,
)
from webapp_api_contract.content_generation import (
    AiGeneratedTextWithSingleImageContentGenerationJobUserInput,
    FromUserMediaTextWithSingleImageContentGenerationJobUserInput,
    ProductLifestyleTextWithSingleImageContentGenerationJobUserInput,
    TextWithSingleImageContentGenerationJobResult,
)
from webapp_api_contract.shared import JobStatus


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
