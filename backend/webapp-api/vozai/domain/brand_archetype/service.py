from vozai.domain.brand_archetype.model import BrandArchetype, BrandArchetypeName
from vozai.domain.brand_archetype.res.archetypes import ARCHETYPE_DATA


def get(name: BrandArchetypeName) -> BrandArchetype | None:
    return ARCHETYPE_DATA.get(name)


def search() -> list[BrandArchetype]:
    return list(ARCHETYPE_DATA.values())
