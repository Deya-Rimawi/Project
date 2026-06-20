from __future__ import annotations

from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class ApplicantType(str, Enum):
    citizen = "citizen"
    lawyer = "lawyer"
    company = "company"
    surveyor = "surveyor"
    authorized_representative = "authorized_representative"


class VerificationState(str, Enum):
    unverified = "unverified"
    verified = "verified"
    suspended = "suspended"


class ApplicantDocument(BaseModel):
    model_config = ConfigDict(use_enum_values=True)

    id: str = Field(description="Unique applicant identifier")
    full_name: str = Field(min_length=2, max_length=200)
    national_id: str = Field(min_length=5, max_length=30)
    email: EmailStr
    phone: str = Field(min_length=7, max_length=25)
    address: str = Field(min_length=3, max_length=300)
    applicant_type: ApplicantType
    verification_state: VerificationState = VerificationState.unverified
    preferred_language: str = Field(default="en", min_length=2, max_length=10)
    notification_preferences: dict[str, bool] = Field(default_factory=lambda: {"email": True, "sms": False, "in_app": True})
    privacy_settings: dict[str, bool] = Field(default_factory=lambda: {"show_contact": False, "show_address": False})
    linked_applications: list[str] = Field(default_factory=list)
    created_at: datetime
    updated_at: datetime
