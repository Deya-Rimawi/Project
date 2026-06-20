from __future__ import annotations

from datetime import datetime, timezone
from uuid import uuid4

from fastapi import HTTPException, status
from pymongo.database import Database

from app.database.mongodb import get_utc_now
from app.schemas.applicant_schema import ApplicantCreate, ApplicantResponse, ApplicantUpdate
from app.utils.validators import (
    ALLOWED_APPLICANT_TYPES,
    ALLOWED_VERIFICATION_STATES,
    enum_value,
    redact_applicant_profile,
    validate_choice,
    validate_national_id,
    validate_phone,
)


class ApplicantService:
    def __init__(self, db: Database) -> None:
        self.db = db

    def create_applicant(self, payload: ApplicantCreate) -> ApplicantResponse:
        validate_national_id(payload.national_id)
        validate_phone(payload.phone)
        validate_choice(enum_value(payload.applicant_type), ALLOWED_APPLICANT_TYPES, "applicant_type")
        validate_choice(enum_value(payload.verification_state), ALLOWED_VERIFICATION_STATES, "verification_state")

        applicants = self.db["applicants"]
        existing = applicants.find_one({"national_id": payload.national_id})
        if existing is not None:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="National ID already exists")

        now = get_utc_now()
        applicant_id = f"app_{uuid4().hex}"
        document = {
            "id": applicant_id,
            "full_name": payload.full_name,
            "national_id": payload.national_id,
            "email": str(payload.email),
            "phone": payload.phone,
            "address": payload.address,
            "applicant_type": enum_value(payload.applicant_type),
            "verification_state": enum_value(payload.verification_state),
            "preferred_language": payload.preferred_language,
            "notification_preferences": payload.notification_preferences,
            "privacy_settings": payload.privacy_settings,
            "linked_applications": payload.linked_applications,
            "created_at": now,
            "updated_at": now,
        }
        applicants.insert_one(document)
        self._log_action("profile_created", applicant_id=applicant_id, details={"full_name": payload.full_name, "national_id": payload.national_id})
        return ApplicantResponse(**document)

    def get_applicant(self, applicant_id: str, include_sensitive: bool = False) -> dict:
        record = self.db["applicants"].find_one({"id": applicant_id})
        if record is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Applicant not found")
        record = redact_applicant_profile(record, include_sensitive)
        return self._serialize(record)

    def list_applicant_applications(self, applicant_id: str) -> list[dict]:
        record = self.db["applicants"].find_one({"id": applicant_id})
        if record is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Applicant not found")

        application_ids = record.get("linked_applications", [])
        summaries: list[dict] = []
        for application_id in application_ids:
            summaries.append(self._application_summary(application_id))
        return summaries

    def update_applicant(self, applicant_id: str, payload: ApplicantUpdate) -> dict:
        existing = self.db["applicants"].find_one({"id": applicant_id})
        if existing is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Applicant not found")

        update_data = payload.model_dump(exclude_unset=True)
        if "phone" in update_data:
            validate_phone(update_data["phone"])
        if "applicant_type" in update_data:
            update_data["applicant_type"] = validate_choice(enum_value(update_data["applicant_type"]), ALLOWED_APPLICANT_TYPES, "applicant_type")
        if "verification_state" in update_data:
            update_data["verification_state"] = validate_choice(enum_value(update_data["verification_state"]), ALLOWED_VERIFICATION_STATES, "verification_state")
        if "email" in update_data:
            update_data["email"] = str(update_data["email"])
        if "linked_applications" in update_data and update_data["linked_applications"] is None:
            update_data["linked_applications"] = []

        update_data["updated_at"] = get_utc_now()
        self.db["applicants"].update_one({"id": applicant_id}, {"$set": update_data})
        updated = self.db["applicants"].find_one({"id": applicant_id})
        return self._serialize(updated or {})

    def _application_summary(self, application_id: str) -> dict:
        documents = list(self.db["application_documents"].find({"application_id": application_id}))
        objections = list(self.db["objections"].find({"application_id": application_id}))
        comments = list(self.db["comments"].find({"application_id": application_id}))
        logs = list(self.db["performance_logs"].find({"application_id": application_id}).sort("timestamp", 1))

        latest_activity = logs[-1]["timestamp"] if logs else None
        current_status = "under_objection" if objections else "submitted"
        return {
            "application_id": application_id,
            "status": current_status,
            "document_count": len(documents),
            "objection_count": len(objections),
            "comment_count": len(comments),
            "latest_activity": latest_activity,
        }

    def _log_action(self, action: str, applicant_id: str | None = None, application_id: str | None = None, details: dict | None = None) -> None:
        self.db["performance_logs"].insert_one(
            {
                "log_id": f"log_{uuid4().hex}",
                "action": action,
                "applicant_id": applicant_id,
                "application_id": application_id,
                "details": details or {},
                "timestamp": get_utc_now(),
            }
        )

    def _serialize(self, document: dict) -> dict:
        serialized = dict(document)
        for key in ("created_at", "updated_at"):
            if isinstance(serialized.get(key), datetime):
                serialized[key] = serialized[key].isoformat()
        return serialized
