from abc import ABC, abstractmethod

from webapp_api_contract.content_generation import (
    ContentGenerationJob,
    TextWithSingleImageContentGenerationJobResult,
)


class BaseTextWithSingleImageContentGenerationJobStrategy(ABC):
    @abstractmethod
    async def generate(
        self, job: ContentGenerationJob
    ) -> TextWithSingleImageContentGenerationJobResult:
        pass
