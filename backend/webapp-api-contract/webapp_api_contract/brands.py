from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field
from pydantic_extra_types.language_code import LanguageAlpha2

from webapp_api_contract.brand_settings import (
    BrandAudience,
    BrandToneOfVoice,
    ContentPillar,
    PositioningBrandData,
)


class BrandArchetypeName(StrEnum):
    INNOCENT = "INNOCENT"
    EVERYMAN = "EVERYMAN"
    HERO = "HERO"
    OUTLAW = "OUTLAW"
    EXPLORER = "EXPLORER"
    CREATOR = "CREATOR"
    RULER = "RULER"
    MAGICIAN = "MAGICIAN"
    LOVER = "LOVER"
    CAREGIVER = "CAREGIVER"
    JESTER = "JESTER"
    SAGE = "SAGE"


class BrandArchetypeData(BaseModel):
    base_human_need: str
    archetype_description: str
    identification_clues: str
    core_shared_values: str
    typical_target_audience: str
    colors_graphics_description: str
    writing_style_description: str
    examples: str

    model_config = ConfigDict(frozen=True)


class BrandArchetype(BaseModel):
    name: BrandArchetypeName
    data: BrandArchetypeData

    model_config = ConfigDict(frozen=True)


class BrandColor(BaseModel):
    name: str
    hex_value: str


class BrandData(BaseModel):
    logo_url: str | None = Field(default=None)
    media_urls: list[str] = Field(default_factory=list)
    colors: list[BrandColor] = Field(default_factory=list)
    brand_mission: str | None = Field(default=None)
    archetype: BrandArchetypeName | None = Field(default=None)
    locale: LanguageAlpha2 | None = Field(default=None)
    audiences: list[BrandAudience] = Field(default_factory=list)
    content_pillars: list[ContentPillar] = Field(default_factory=list)
    tone_of_voice: BrandToneOfVoice = Field(default_factory=BrandToneOfVoice)
    positioning: PositioningBrandData = Field(default_factory=PositioningBrandData)

    model_config = ConfigDict(from_attributes=True)


class Brand(BaseModel):
    id: str
    user_id: str
    name: str
    data: BrandData = Field(default_factory=BrandData)
    created_at: datetime
    updated_at: datetime


class BrandCreateRequest(BaseModel):
    name: str
    data: BrandData

    model_config = ConfigDict(from_attributes=True)


class BrandSearchRequest(BaseModel):
    user_id: str
    name: str | None = None
    limit: int | None = Field(default=5, ge=1, le=1000)
    offset: int | None = Field(default=0, ge=0)


class BrandResponse(BaseModel):
    id: str
    name: str
    data: BrandData | None = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class BrandUpdateRequest(BaseModel):
    name: str | None = None
    data: BrandData | None = None

    model_config = ConfigDict(from_attributes=True)
