from __future__ import annotations

from fastapi import APIRouter, Depends, Query
from pymongo.database import Database

from app.database.mongodb import get_database
from app.schemas.applicant_schema import ApplicantCreate, ApplicantResponse, ApplicantUpdate
from app.services.applicant_service import ApplicantService

router = APIRouter(prefix="/applicants")


@router.post("", response_model=ApplicantResponse, summary="Create applicant profile")
def create_applicant(payload: ApplicantCreate, db: Database = Depends(get_database)) -> ApplicantResponse:
    return ApplicantService(db).create_applicant(payload)


@router.get("/{applicant_id}", summary="Get applicant profile")
def get_applicant(
    applicant_id: str,
    include_sensitive: bool = Query(default=False, description="Return sensitive profile fields when true"),
    db: Database = Depends(get_database),
) -> dict:
    return ApplicantService(db).get_applicant(applicant_id, include_sensitive=include_sensitive)


@router.get("/{applicant_id}/applications", summary="List applicant applications")
def get_applicant_applications(applicant_id: str, db: Database = Depends(get_database)) -> list[dict]:
    return ApplicantService(db).list_applicant_applications(applicant_id)


@router.patch("/{applicant_id}", summary="Update applicant profile")
def update_applicant(applicant_id: str, payload: ApplicantUpdate, db: Database = Depends(get_database)) -> dict:
    return ApplicantService(db).update_applicant(applicant_id, payload)
