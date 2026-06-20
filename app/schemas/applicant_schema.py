from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field
from pydantic import field_validator

from app.models.applicant import ApplicantType, VerificationState
from app.utils.validators import NATIONAL_ID_PATTERN, PHONE_PATTERN


class ApplicantCreate(BaseModel):
    full_name: str = Field(..., description="Applicant full name", examples=["Amina Rahman"])
    national_id: str = Field(..., description="Unique national ID", examples=["1998-01-123456"])
    email: EmailStr = Field(..., description="Applicant email address", examples=["amina@example.com"])
    phone: str = Field(..., description="Applicant phone number", examples=["+94771234567"])
    address: str = Field(..., description="Applicant address", examples=["12 Galle Road, Colombo"])
    applicant_type: ApplicantType = Field(..., description="Applicant classification")
    verification_state: VerificationState = Field(default=VerificationState.unverified, description="Verification state")
    preferred_language: str = Field(default="en", description="Preferred language code", examples=["en"])
    notification_preferences: dict[str, bool] = Field(
        default_factory=lambda: {"email": True, "sms": False, "in_app": True},
        description="Notification delivery preferences",
    )
    privacy_settings: dict[str, bool] = Field(
        default_factory=lambda: {"show_contact": False, "show_address": False},
        description="Privacy visibility settings",
    )
    linked_applications: list[str] = Field(default_factory=list, description="Linked application identifiers")

    model_config = ConfigDict(use_enum_values=True)

    @field_validator("national_id")
    @classmethod
    def validate_national_id(cls, value: str) -> str:
        if not NATIONAL_ID_PATTERN.match(value):
            raise ValueError("National ID format is invalid")
        return value

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, value: str) -> str:
        if not PHONE_PATTERN.match(value):
            raise ValueError("Phone number must be in a valid international or local format")
        return value


class ApplicantUpdate(BaseModel):
    full_name: str | None = Field(default=None, description="Applicant full name")
    email: EmailStr | None = Field(default=None, description="Applicant email address")
    phone: str | None = Field(default=None, description="Applicant phone number")
    address: str | None = Field(default=None, description="Applicant address")
    applicant_type: ApplicantType | None = Field(default=None, description="Applicant classification")
    verification_state: VerificationState | None = Field(default=None, description="Verification state")
    preferred_language: str | None = Field(default=None, description="Preferred language code")
    notification_preferences: dict[str, bool] | None = Field(default=None, description="Notification preferences")
    privacy_settings: dict[str, bool] | None = Field(default=None, description="Privacy settings")
    linked_applications: list[str] | None = Field(default=None, description="Linked application identifiers")

    model_config = ConfigDict(use_enum_values=True)

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, value: str | None) -> str | None:
        if value is not None and not PHONE_PATTERN.match(value):
            raise ValueError("Phone number must be in a valid international or local format")
        return value


class ApplicantResponse(BaseModel):
    id: str
    full_name: str
    national_id: str
    email: EmailStr
    phone: str
    address: str
    applicant_type: ApplicantType
    verification_state: VerificationState
    preferred_language: str
    notification_preferences: dict[str, bool]
    privacy_settings: dict[str, bool]
    linked_applications: list[str]
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(use_enum_values=True)
