from abc import ABC, abstractmethod

from webapp_api_contract.brand_extraction import (
    BrandGenerationJob,
    BrandGenerationResult,
)


class BrandGenerationBaseStep(ABC):
    @abstractmethod
    async def execute(self, job: BrandGenerationJob) -> BrandGenerationResult:
        raise NotImplementedError("execute method must be implemented by subclasses")
