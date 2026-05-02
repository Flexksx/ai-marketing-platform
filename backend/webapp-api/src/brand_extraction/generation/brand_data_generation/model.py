import public
from pydantic import BaseModel, ConfigDict, Field
from pydantic_extra_types.language_code import LanguageAlpha2

from webapp_api_contract.brands import BrandColor
from webapp_api_contract.brands import BrandArchetypeName
from webapp_api_contract.brand_settings import (
    BrandAudience,
    ContentPillar,
    SentenceLengthPreference,
)


@public.add
class BrandGenerationJobTextualDescriptionResult(BaseModel):
    name: str = Field(...)
    colors: list[BrandColor] = Field(...)
    locale: LanguageAlpha2 = Field(...)
    brand_mission: str = Field(...)
    description: str = Field(..., max_length=1000)
    archetype: BrandArchetypeName = Field(...)

    model_config = ConfigDict(from_attributes=True)


@public.add
class BrandGenerationJobToneOfVoiceProfilingResult(BaseModel):
    industry_jargon_usage_level: int = Field(..., min=1, max=4)
    sentence_length_preference: SentenceLengthPreference = Field(...)
    formality_level: int = Field(..., min=1, max=4)
    humour_level: int = Field(..., min=1, max=4)
    irreverence_level: int = Field(..., min=1, max=4)
    enthusiasm_level: int = Field(..., min=1, max=4)
    sensory_keywords: list[str] = Field(..., min_length=3, max_length=8)
    excluded_words: list[str] = Field(..., min_length=3, max_length=10)
    signature_words: list[str] = Field(..., min_length=3, max_length=10)

    model_config = ConfigDict(from_attributes=True)


@public.add
class PositioningBrandDataResult(BaseModel):
    points_of_parity: list[str] = Field(..., min_length=2, max_length=5)
    points_of_difference: list[str] = Field(..., min_length=2, max_length=8)
    product_description: str = Field(...)


@public.add
class BrandGenerationContentPillarResult(BaseModel):
    content_pillars: list[ContentPillar] = Field(...)


@public.add
class BrandGenerationJobAudienceProfilingResult(BaseModel):
    audiences: list[BrandAudience] = Field(...)
