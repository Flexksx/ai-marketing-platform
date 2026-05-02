from pydantic import BaseModel, ConfigDict

from webapp_api_contract.brand.archetype import BrandArchetypeName


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
