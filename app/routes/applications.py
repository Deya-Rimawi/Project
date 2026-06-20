from __future__ import annotations

from fastapi import APIRouter, Depends
from pymongo.database import Database

from app.database.mongodb import get_database
from app.schemas.comment_schema import CommentCreate, CommentResponse
from app.schemas.document_schema import DocumentCreate, DocumentResponse
from app.schemas.objection_schema import ObjectionCreate, ObjectionResponse
from app.schemas.timeline_schema import TimelineResponse
from app.services.document_service import DocumentService
from app.services.objection_service import ObjectionService
from app.services.timeline_service import TimelineService

router = APIRouter(prefix="/applications")


@router.post("/{application_id}/documents", response_model=DocumentResponse, summary="Upload document metadata")
def upload_document(
    application_id: str,
    payload: DocumentCreate,
    db: Database = Depends(get_database),
) -> DocumentResponse:
    return DocumentService(db).add_document(application_id, payload)


@router.post("/{application_id}/comments", response_model=CommentResponse, summary="Add application comment")
def add_comment(
    application_id: str,
    payload: CommentCreate,
    db: Database = Depends(get_database),
) -> CommentResponse:
    return TimelineService(db).add_comment(application_id, payload)


@router.post("/{application_id}/objections", response_model=ObjectionResponse, summary="Submit objection")
def submit_objection(
    application_id: str,
    payload: ObjectionCreate,
    db: Database = Depends(get_database),
) -> ObjectionResponse:
    return ObjectionService(db).submit_objection(application_id, payload)


@router.get("/{application_id}/timeline", response_model=TimelineResponse, summary="Get application timeline")
def get_timeline(application_id: str, db: Database = Depends(get_database)) -> TimelineResponse:
    return TimelineService(db).get_timeline(application_id)
