from datetime import datetime

import public
from pydantic import BaseModel, ConfigDict, Field
from pydantic_extra_types.language_code import LanguageAlpha2

from webapp_api_contract.brands import BrandArchetypeName
from webapp_api_contract.brand_settings import (
    BrandAudience,
    BrandToneOfVoice,
    ContentPillar,
    PositioningBrandData,
)


@public.add
class BrandColor(BaseModel):
    name: str
    hex_value: str


@public.add
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


@public.add
class Brand(BaseModel):
    id: str
    user_id: str
    name: str
    data: BrandData = Field(default_factory=BrandData)
    created_at: datetime
    updated_at: datetime
