from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class CommentCreate(BaseModel):
    author: str = Field(..., description="Comment author", examples=["Amina Rahman"])
    comment_text: str = Field(..., description="Comment body", examples=["Please review the boundary map attached."])

    model_config = ConfigDict()


class CommentResponse(BaseModel):
    comment_id: str
    application_id: str
    author: str
    comment_text: str
    created_at: datetime

    model_config = ConfigDict()
