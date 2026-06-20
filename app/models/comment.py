from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class CommentDocument(BaseModel):
    model_config = ConfigDict(use_enum_values=True)

    comment_id: str = Field(description="Unique comment identifier")
    application_id: str
    author: str = Field(description="Author name or applicant identifier")
    comment_text: str = Field(min_length=1, max_length=4000)
    created_at: datetime
