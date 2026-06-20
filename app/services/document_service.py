from __future__ import annotations

from uuid import uuid4

from fastapi import HTTPException, status
from pymongo.database import Database

from app.database.mongodb import get_utc_now
from app.schemas.document_schema import DocumentCreate, DocumentResponse
from app.utils.validators import ALLOWED_REVIEW_STATUSES, enum_value, validate_choice


class DocumentService:
    def __init__(self, db: Database) -> None:
        self.db = db

    def add_document(self, application_id: str, payload: DocumentCreate) -> DocumentResponse:
        validate_choice(enum_value(payload.review_status), ALLOWED_REVIEW_STATUSES, "review_status")

        document = {
            "document_id": f"doc_{uuid4().hex}",
            "application_id": application_id,
            "document_type": payload.document_type,
            "file_name": payload.file_name,
            "upload_date": get_utc_now(),
            "review_status": enum_value(payload.review_status),
            "uploaded_by": payload.uploaded_by,
        }
        self.db["application_documents"].insert_one(document)
        self._log_action("document_uploaded", application_id=application_id, applicant_id=payload.uploaded_by, details=document)
        return DocumentResponse(**document)

    def _log_action(self, action: str, application_id: str | None = None, applicant_id: str | None = None, details: dict | None = None) -> None:
        self.db["performance_logs"].insert_one(
            {
                "log_id": f"log_{uuid4().hex}",
                "action": action,
                "application_id": application_id,
                "applicant_id": applicant_id,
                "details": details or {},
                "timestamp": get_utc_now(),
            }
        )
