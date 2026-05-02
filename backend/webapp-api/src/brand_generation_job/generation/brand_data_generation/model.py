import public
from pydantic import BaseModel, ConfigDict, Field
from pydantic_extra_types.language_code import LanguageAlpha2

from webapp_api_contract.brand import BrandColor
from webapp_api_contract.brand.archetype import BrandArchetypeName
from webapp_api_contract.brand.audience import BrandAudience
from webapp_api_contract.brand.content_pillar import ContentPillar


@public.add
class BrandGenerationJobTextualDescriptionResult(BaseModel):
    name: str = Field(...)
    colors: list[BrandColor] = Field(...)
    locale: LanguageAlpha2 = Field(...)
    brand_mission: str = Field(...)
    description: str = Field(..., max_length=1000)

    model_config = ConfigDict(from_attributes=True)


@public.add
class BrandGenerationJobToneOfVoiceProfilingResult(BaseModel):
    archetype: BrandArchetypeName = Field(...)
    jargon_density: int = Field(..., ge=1, le=4)
    visual_density: int = Field(..., ge=1, le=4)
    must_use_words: list[str] = Field(..., min_length=3, max_length=10)
    forbidden_words: list[str] = Field(..., min_length=3, max_length=10)

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
