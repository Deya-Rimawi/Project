from __future__ import annotations

from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field


class ObjectionStatus(str, Enum):
    submitted = "submitted"
    under_review = "under_review"
    resolved = "resolved"
    rejected = "rejected"
    withdrawn = "withdrawn"


class ObjectionDocument(BaseModel):
    model_config = ConfigDict(use_enum_values=True)

    objection_id: str = Field(description="Unique objection identifier")
    application_id: str
    applicant_id: str
    reason: str = Field(min_length=5, max_length=2000)
    attachments: list[str] = Field(default_factory=list)
    status: ObjectionStatus = ObjectionStatus.submitted
    created_at: datetime
