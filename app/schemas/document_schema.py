from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.models.document import ReviewStatus


class DocumentCreate(BaseModel):
    document_type: str = Field(..., description="Type of document", examples=["title_deed"])
    file_name: str = Field(..., description="Stored file name", examples=["title_deed.pdf"])
    review_status: ReviewStatus = Field(default=ReviewStatus.pending, description="Current document review status")
    uploaded_by: str | None = Field(default=None, description="Uploader identifier")

    model_config = ConfigDict(use_enum_values=True)


class DocumentResponse(BaseModel):
    document_id: str
    application_id: str
    document_type: str
    file_name: str
    upload_date: datetime
    review_status: ReviewStatus
    uploaded_by: str | None = None

    model_config = ConfigDict(use_enum_values=True)
