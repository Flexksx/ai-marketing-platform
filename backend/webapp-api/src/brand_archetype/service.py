from src.brand_archetype.res.archetypes import ARCHETYPE_DATA
from webapp_api_contract.brands import BrandArchetype, BrandArchetypeName


def get(name: BrandArchetypeName) -> BrandArchetype | None:
    return ARCHETYPE_DATA.get(name)


def search() -> list[BrandArchetype]:
    return list(ARCHETYPE_DATA.values())
