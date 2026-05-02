from pydantic import BaseModel, ConfigDict, Field

from webapp_api_contract.brand.archetype import BrandArchetypeName


class BrandToneOfVoice(BaseModel):
    archetype: BrandArchetypeName | None = Field(default=None)
    jargon_density: int = Field(default=1, ge=1, le=4)
    visual_density: int = Field(default=1, ge=1, le=4)
    must_use_words: list[str] = Field(default_factory=list)
    forbidden_words: list[str] = Field(default_factory=list)

    model_config = ConfigDict(frozen=True)
