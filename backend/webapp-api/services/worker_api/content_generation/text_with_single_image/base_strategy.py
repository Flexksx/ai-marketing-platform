from abc import ABC, abstractmethod

from aimarketing.domain.content_generation_job import (
    ContentGenerationJob,
    TextWithSingleImageContentGenerationJobResult,
)


class BaseTextWithSingleImageContentGenerationJobStrategy(ABC):
    @abstractmethod
    async def generate(
        self, job: ContentGenerationJob
    ) -> TextWithSingleImageContentGenerationJobResult:
        pass
