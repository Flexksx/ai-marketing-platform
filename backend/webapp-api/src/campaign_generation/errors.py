import public
from fastapi import HTTPException, status


@public.add
class CampaignGenerationJobNotFoundException(HTTPException):
    def __init__(self, job_id: str):
        self.job_id = job_id
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Campaign creation job with id {job_id} not found",
        )


@public.add
class CampaignGenerationJobResultNotFoundException(HTTPException):
    def __init__(self, job_id: str):
        self.job_id = job_id
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Campaign creation job result with id {job_id} not found",
        )


@public.add
class CampaignGenerationJobResultElementNotFoundException(HTTPException):
    def __init__(self, job_id: str, element_name: str):
        self.job_id = job_id
        self.element_name = element_name
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Campaign creation job result element {element_name} with id {job_id} not found",
        )


@public.add
class CampaignGenerationJobWorkflowTypeMismatchException(HTTPException):
    def __init__(self, message: str):
        self.message = message
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Campaign creation job workflow type mismatch. {message}",
        )


@public.add
class CampaignGenerationJobCreationFailedException(HTTPException):
    def __init__(
        self,
    ):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Campaign generation job start failed",
        )


@public.add
class PostingPlanItemNotFoundException(HTTPException):
    def __init__(self, job_id: str, item_id: str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Posting plan item {item_id} not found for job {job_id}",
        )


@public.add
class ContentPlanItemMissingContentDataException(HTTPException):
    def __init__(self, job_id: str, item_id: str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Content plan item {item_id} has no content_data for job {job_id}",
        )


@public.add
class OptimisticLockError(Exception):
    pass
