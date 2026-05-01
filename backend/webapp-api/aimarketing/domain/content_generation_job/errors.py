import public
from fastapi import HTTPException, status

from aimarketing.domain.content_generation_job.enum import ContentGenerationJobWorkflowType


@public.add
class ContentGenerationJobNotFoundException(HTTPException):
    def __init__(self, job_id: str):
        self.job_id = job_id
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Content generation job with id {job_id} not found",
        )


@public.add
class ContentGenerationJobInvalidUserInputException(HTTPException):
    def __init__(self, job_id: str, message: str):
        self.job_id = job_id
        self.message = message
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Content generation job {job_id} has invalid user input: {message}",
        )


@public.add
class ContentGenerationJobUnsupportedWorkflowTypeException(HTTPException):
    def __init__(self, job_id: str, workflow_type: ContentGenerationJobWorkflowType):
        self.job_id = job_id
        self.workflow_type = workflow_type
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Content generation job {job_id} has unsupported workflow type: {workflow_type}",
        )


@public.add
class ContentGenerationJobRuntimeException(HTTPException):
    def __init__(self, job_id: str, error: Exception):
        self.job_id = job_id
        self.error = error
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process content generation job {job_id}: {error}",
        )


@public.add
class ContentGenerationJobNoResultException(HTTPException):
    def __init__(self, job_id: str):
        self.job_id = job_id
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Content generation job {job_id} has no result",
        )
