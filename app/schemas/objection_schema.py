from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.models.objection import ObjectionStatus


class ObjectionCreate(BaseModel):
    applicant_id: str = Field(..., description="Applicant raising the objection")
    reason: str = Field(..., description="Reason for the objection", examples=["Boundary dispute raised by neighbor"])
    attachments: list[str] = Field(default_factory=list, description="Supporting document file names")
    status: ObjectionStatus = Field(default=ObjectionStatus.submitted, description="Objection status")

    model_config = ConfigDict(use_enum_values=True)


class ObjectionResponse(BaseModel):
    objection_id: str
    application_id: str
    applicant_id: str
    reason: str
    attachments: list[str]
    status: ObjectionStatus
    created_at: datetime

    model_config = ConfigDict(use_enum_values=True)
