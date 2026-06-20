from __future__ import annotations

from uuid import uuid4

from fastapi import HTTPException, status
from pymongo.database import Database

from app.database.mongodb import get_utc_now
from app.schemas.comment_schema import CommentCreate, CommentResponse
from app.schemas.timeline_schema import TimelineResponse


class TimelineService:
    def __init__(self, db: Database) -> None:
        self.db = db

    def add_comment(self, application_id: str, payload: CommentCreate) -> CommentResponse:
        comment = {
            "comment_id": f"cmt_{uuid4().hex}",
            "application_id": application_id,
            "author": payload.author,
            "comment_text": payload.comment_text,
            "created_at": get_utc_now(),
        }
        self.db["comments"].insert_one(comment)
        self.db["performance_logs"].insert_one(
            {
                "log_id": f"log_{uuid4().hex}",
                "action": "comment_added",
                "application_id": application_id,
                "applicant_id": None,
                "details": {"comment_id": comment["comment_id"], "author": payload.author},
                "timestamp": comment["created_at"],
            }
        )
        return CommentResponse(**comment)

    def get_timeline(self, application_id: str) -> TimelineResponse:
        documents = list(self.db["application_documents"].find({"application_id": application_id}).sort("upload_date", 1))
        objections = list(self.db["objections"].find({"application_id": application_id}).sort("created_at", 1))
        comments = list(self.db["comments"].find({"application_id": application_id}).sort("created_at", 1))
        logs = list(self.db["performance_logs"].find({"application_id": application_id}).sort("timestamp", 1))

        timestamps = [entry["timestamp"] for entry in logs if entry.get("timestamp") is not None]
        status_history = [self._serialize_log(entry) for entry in logs]
        return TimelineResponse(
            application_id=application_id,
            status_history=status_history,
            document_uploads=[self._serialize_document(document) for document in documents],
            objections=[self._serialize_document(objection) for objection in objections],
            comments=[self._serialize_document(comment) for comment in comments],
            timestamps=timestamps,
        )

    def _serialize_document(self, document: dict) -> dict:
        serialized = dict(document)
        for key, value in list(serialized.items()):
            if hasattr(value, "isoformat"):
                serialized[key] = value.isoformat()
        return serialized

    def _serialize_log(self, document: dict) -> dict:
        serialized = dict(document)
        if hasattr(serialized.get("timestamp"), "isoformat"):
            serialized["timestamp"] = serialized["timestamp"].isoformat()
        return serialized
