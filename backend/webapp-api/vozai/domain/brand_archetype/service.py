from vozai.domain.brand_archetype.model import BrandArchetype, BrandArchetypeName
from vozai.domain.brand_archetype.res.archetypes import (
    ARCHETYPE_DATA,
)


class BrandArchetypeService:
    def __init__(self):
        self.__data = ARCHETYPE_DATA

    def get(self, name: BrandArchetypeName) -> BrandArchetype | None:
        return self.__data.get(name)

    def search(self) -> list[BrandArchetype]:
        return list(self.__data.values())
