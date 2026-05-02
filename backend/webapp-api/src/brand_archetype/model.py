from enum import StrEnum

from pydantic import BaseModel, ConfigDict


class BrandArchetypeData(BaseModel):
    base_human_need: str
    archetype_description: str
    identification_clues: str
    core_shared_values: str
    typical_target_audience: str
    colors_graphics_description: str
    writing_style_description: str
    examples: str


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


class BrandArchetype(BaseModel):
    model_config = ConfigDict(frozen=True)
    name: BrandArchetypeName
    data: BrandArchetypeData
