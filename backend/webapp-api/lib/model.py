from enum import StrEnum


class JobStatus(StrEnum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    FAILED = "failed"
    ACCEPTED = "accepted"


class ContentChannelName(StrEnum):
    INSTAGRAM = "INSTAGRAM"
    LINKEDIN = "LINKEDIN"


class ContentFormat(StrEnum):
    TEXT = "TEXT"
    TEXT_WITH_SINGLE_IMAGE = "TEXT_WITH_SINGLE_IMAGE"
