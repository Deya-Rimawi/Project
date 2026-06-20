from __future__ import annotations

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pymongo.errors import DuplicateKeyError, PyMongoError

from app.database.mongodb import init_database, close_database
from app.routes.applicants import router as applicants_router
from app.routes.applications import router as applications_router

app = FastAPI(
    title="LRMIS Applicant Portal and Profiles Module",
    version="1.0.0",
    description="Applicant portal, profiles, documents, objections, comments, and timeline APIs for LRMIS.",
)


@app.on_event("startup")
def startup_event() -> None:
    init_database()


@app.on_event("shutdown")
def shutdown_event() -> None:
    close_database()


@app.exception_handler(DuplicateKeyError)
def duplicate_key_handler(_: Request, exc: DuplicateKeyError) -> JSONResponse:
    return JSONResponse(status_code=409, content={"detail": "Duplicate key error", "error": str(exc)})


@app.exception_handler(PyMongoError)
def mongo_error_handler(_: Request, exc: PyMongoError) -> JSONResponse:
    return JSONResponse(status_code=500, content={"detail": "Database error", "error": str(exc)})


@app.exception_handler(Exception)
def generic_error_handler(_: Request, exc: Exception) -> JSONResponse:
    return JSONResponse(status_code=500, content={"detail": "Internal server error", "error": str(exc)})


@app.get("/", tags=["Health"])
def root() -> dict[str, str]:
    return {"message": "LRMIS Applicant Portal and Profiles Module is running"}


app.include_router(applicants_router, tags=["Applicants"])
app.include_router(applications_router, tags=["Applications"])
