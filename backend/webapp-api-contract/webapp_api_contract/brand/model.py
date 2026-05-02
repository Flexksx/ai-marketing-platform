from pydantic import BaseModel, ConfigDict, Field
from pydantic_extra_types.language_code import LanguageAlpha2

from webapp_api_contract.brand.audience import BrandAudience
from webapp_api_contract.brand.content_pillar import ContentPillar
from webapp_api_contract.brand.positioning import PositioningBrandData
from webapp_api_contract.brand.tone_of_voice import BrandToneOfVoice


class BrandColor(BaseModel):
    name: str
    hex_value: str


class BrandData(BaseModel):
    logo_url: str | None = Field(default=None)
    website_url: str | None = Field(default=None)
    media_urls: list[str] = Field(default_factory=list)
    colors: list[BrandColor] = Field(default_factory=list)
    brand_mission: str | None = Field(default=None)
    locale: LanguageAlpha2 | None = Field(default=None)
    audiences: list[BrandAudience] = Field(default_factory=list)
    content_pillars: list[ContentPillar] = Field(default_factory=list)
    tone_of_voice: BrandToneOfVoice = Field(default_factory=BrandToneOfVoice)
    positioning: PositioningBrandData = Field(default_factory=PositioningBrandData)

    model_config = ConfigDict(from_attributes=True)
