from enum import StrEnum

import public


@public.add
class JobStatus(StrEnum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    FAILED = "failed"
    ACCEPTED = "accepted"
