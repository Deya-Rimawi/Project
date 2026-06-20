from __future__ import annotations

import re
from typing import Any

from fastapi import HTTPException, status

ALLOWED_APPLICANT_TYPES = {
    "citizen",
    "lawyer",
    "company",
    "surveyor",
    "authorized_representative",
}

ALLOWED_VERIFICATION_STATES = {"unverified", "verified", "suspended"}
ALLOWED_REVIEW_STATUSES = {"pending", "under_review", "approved", "rejected"}
ALLOWED_OBJECTION_STATUSES = {"submitted", "under_review", "resolved", "rejected", "withdrawn"}

PHONE_PATTERN = re.compile(r"^\+?[0-9][0-9\s\-()]{7,19}$")
NATIONAL_ID_PATTERN = re.compile(r"^[A-Za-z0-9\-/.]{5,30}$")


def validate_phone(phone: str) -> str:
    if not PHONE_PATTERN.match(phone):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Phone number must be in a valid international or local format.",
        )
    return phone


def validate_national_id(national_id: str) -> str:
    if not NATIONAL_ID_PATTERN.match(national_id):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="National ID format is invalid.",
        )
    return national_id


def validate_choice(value: str, allowed_values: set[str], field_name: str) -> str:
    if hasattr(value, "value"):
        value = value.value
    if value not in allowed_values:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"{field_name} must be one of: {', '.join(sorted(allowed_values))}",
        )
    return value


def enum_value(value: Any) -> Any:
    return value.value if hasattr(value, "value") else value


def redact_applicant_profile(applicant: dict[str, Any], include_sensitive: bool) -> dict[str, Any]:
    if include_sensitive:
        return applicant

    safe_profile = dict(applicant)
    for key in ("national_id", "email", "phone", "address"):
        safe_profile.pop(key, None)
    return safe_profile
