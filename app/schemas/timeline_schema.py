from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class TimelineResponse(BaseModel):
    application_id: str = Field(description="Application identifier")
    status_history: list[dict[str, Any]] = Field(default_factory=list, description="Status and activity history")
    document_uploads: list[dict[str, Any]] = Field(default_factory=list, description="Uploaded document events")
    objections: list[dict[str, Any]] = Field(default_factory=list, description="Objection records")
    comments: list[dict[str, Any]] = Field(default_factory=list, description="Comment records")
    timestamps: list[datetime] = Field(default_factory=list, description="Chronological timestamps used by the timeline")

    model_config = ConfigDict()
