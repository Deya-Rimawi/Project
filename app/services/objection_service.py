from __future__ import annotations

from uuid import uuid4

from fastapi import HTTPException, status
from pymongo.database import Database

from app.database.mongodb import get_utc_now
from app.schemas.objection_schema import ObjectionCreate, ObjectionResponse
from app.utils.validators import ALLOWED_OBJECTION_STATUSES, enum_value, validate_choice


class ObjectionService:
    def __init__(self, db: Database) -> None:
        self.db = db

    def submit_objection(self, application_id: str, payload: ObjectionCreate) -> ObjectionResponse:
        validate_choice(enum_value(payload.status), ALLOWED_OBJECTION_STATUSES, "objection status")

        applicant = self.db["applicants"].find_one({"id": payload.applicant_id})
        if applicant is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Applicant not found")

        objection_id = f"obj_{uuid4().hex}"
        document = {
            "objection_id": objection_id,
            "application_id": application_id,
            "applicant_id": payload.applicant_id,
            "reason": payload.reason,
            "attachments": payload.attachments,
            "status": enum_value(payload.status),
            "created_at": get_utc_now(),
        }
        self.db["objections"].insert_one(document)
        self._mark_application_under_objection(application_id, payload.applicant_id, objection_id)
        return ObjectionResponse(**document)

    def _mark_application_under_objection(self, application_id: str, applicant_id: str, objection_id: str) -> None:
        self.db["performance_logs"].insert_one(
            {
                "log_id": f"log_{uuid4().hex}",
                "action": "objection_submitted",
                "application_id": application_id,
                "applicant_id": applicant_id,
                "details": {"objection_id": objection_id, "status": "under_objection"},
                "timestamp": get_utc_now(),
            }
        )
        self.db["performance_logs"].insert_one(
            {
                "log_id": f"log_{uuid4().hex}",
                "action": "application_status_changed",
                "application_id": application_id,
                "applicant_id": applicant_id,
                "details": {"status": "under_objection", "objection_id": objection_id},
                "timestamp": get_utc_now(),
            }
        )
