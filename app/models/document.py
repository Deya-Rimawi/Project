from __future__ import annotations

from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field


class ReviewStatus(str, Enum):
    pending = "pending"
    under_review = "under_review"
    approved = "approved"
    rejected = "rejected"


class DocumentDocument(BaseModel):
    model_config = ConfigDict(use_enum_values=True)

    document_id: str = Field(description="Unique document identifier")
    application_id: str
    document_type: str = Field(min_length=2, max_length=100)
    file_name: str = Field(min_length=1, max_length=255)
    upload_date: datetime
    review_status: ReviewStatus = ReviewStatus.pending
    uploaded_by: str | None = None
