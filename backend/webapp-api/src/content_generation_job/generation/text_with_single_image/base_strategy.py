from abc import ABC, abstractmethod

from src.content_generation_job.model import ContentGenerationJob
from webapp_api_contract.content_generation import (
    TextWithSingleImageContentGenerationJobResult,
)


class BaseTextWithSingleImageContentGenerationJobStrategy(ABC):
    @abstractmethod
    async def generate(
        self, job: ContentGenerationJob
    ) -> TextWithSingleImageContentGenerationJobResult:
        pass
