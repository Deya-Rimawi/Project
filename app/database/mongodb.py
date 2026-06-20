from __future__ import annotations

import os
from datetime import datetime, timezone
from typing import Any

from pymongo import ASCENDING, MongoClient
from pymongo.database import Database
from pymongo.errors import ServerSelectionTimeoutError

_client: MongoClient | None = None
_database: Database | None = None


def get_utc_now() -> datetime:
    return datetime.now(timezone.utc)


def get_database() -> Database:
    if _database is None:
        raise RuntimeError("MongoDB database is not initialized")
    return _database


def init_database() -> None:
    global _client, _database

    if _client is not None and _database is not None:
        return

    mongo_uri = (
        os.getenv("MONGODB_URI", "")
        or os.getenv("MONGO_URI", "")
    ).strip()
    database_name = (
        os.getenv("MONGODB_DB", "")
        or os.getenv("DB_NAME", "")
        or "LRMIS_DB"
    ).strip()
    server_selection_timeout_ms = int(os.getenv("MONGODB_SERVER_SELECTION_TIMEOUT_MS", "5000"))

    if not mongo_uri:
        raise RuntimeError(
            "MONGODB_URI is not set. Configure it in your environment before starting the API."
        )

    _client = MongoClient(mongo_uri, serverSelectionTimeoutMS=server_selection_timeout_ms)
    try:
        # Force early connection validation during startup.
        _client.admin.command("ping")
        _database = _client[database_name]
        _create_indexes(_database)
    except ServerSelectionTimeoutError as exc:
        close_database()
        atlas_hint = ""
        if mongo_uri.startswith("mongodb+srv://"):
            atlas_hint = (
                " Atlas checklist: add your current public IP in Atlas Network Access, "
                "confirm the cluster is not paused, and disable VPN/proxy/SSL inspection if enabled."
            )
        raise RuntimeError(
            f"Could not connect to MongoDB at '{mongo_uri}'."
            " Verify URI/credentials and network reachability."
            f"{atlas_hint}"
        ) from exc


def close_database() -> None:
    global _client, _database

    if _client is not None:
        _client.close()
    _client = None
    _database = None


def _create_indexes(database: Database) -> None:
    database["applicants"].create_index([("national_id", ASCENDING)], unique=True, name="uq_national_id")
    database["applicants"].create_index([("email", ASCENDING)], name="idx_applicant_email")
    database["applicants"].create_index([("applicant_type", ASCENDING)], name="idx_applicant_type")
    database["applicants"].create_index([("verification_state", ASCENDING)], name="idx_verification_state")

    database["application_documents"].create_index([("application_id", ASCENDING), ("upload_date", ASCENDING)], name="idx_documents_application_date")
    database["application_documents"].create_index([("review_status", ASCENDING)], name="idx_documents_review_status")

    database["comments"].create_index([("application_id", ASCENDING), ("created_at", ASCENDING)], name="idx_comments_application_date")

    database["objections"].create_index([("objection_id", ASCENDING)], unique=True, name="uq_objection_id")
    database["objections"].create_index([("application_id", ASCENDING), ("created_at", ASCENDING)], name="idx_objections_application_date")
    database["objections"].create_index([("applicant_id", ASCENDING)], name="idx_objections_applicant")

    database["performance_logs"].create_index([("action", ASCENDING), ("timestamp", ASCENDING)], name="idx_logs_action_timestamp")
    database["performance_logs"].create_index([("application_id", ASCENDING), ("timestamp", ASCENDING)], name="idx_logs_application_timestamp")
    database["performance_logs"].create_index([("applicant_id", ASCENDING), ("timestamp", ASCENDING)], name="idx_logs_applicant_timestamp")
