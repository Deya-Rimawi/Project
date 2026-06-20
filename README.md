# COMP4382 LRMIS - Student 2 Module

Applicant Portal and Profiles Module for the Land Registration Management Information System (LRMIS).

## Tech Stack

- FastAPI
- MongoDB with PyMongo
- Pydantic
- Python 3.12+

## Features

- Applicant profile creation and retrieval
- National ID uniqueness validation
- Document uploads by application
- Applicant comments on applications
- Objection submission with generated objection IDs
- Timeline aggregation for applications
- MongoDB indexes and performance logging
- Swagger/OpenAPI documentation

## Project Structure

```text
app/
├── main.py
├── database/
│   └── mongodb.py
├── models/
│   ├── applicant.py
│   ├── comment.py
│   ├── document.py
│   └── objection.py
├── schemas/
│   ├── applicant_schema.py
│   ├── comment_schema.py
│   ├── document_schema.py
│   └── objection_schema.py
├── routes/
│   ├── applicants.py
│   └── applications.py
├── services/
│   ├── applicant_service.py
│   ├── document_service.py
│   ├── objection_service.py
│   └── timeline_service.py
└── utils/
    └── validators.py
```

## Setup

1. Create and activate a Python virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Set MongoDB environment variables if needed:

```bash
set MONGODB_URI=mongodb://localhost:27017
set MONGODB_DB=lrmis
```

4. Run the API:

```bash
uvicorn app.main:app --reload
```

5. Open Swagger UI at:

```text
http://127.0.0.1:8000/docs
```

## Environment Variables

- `MONGODB_URI`: MongoDB connection string. Defaults to `mongodb://localhost:27017`
- `MONGODB_DB`: Database name. Defaults to `lrmis`

## API Endpoints

### Applicant Profile

- `POST /applicants`
- `GET /applicants/{applicant_id}`
- `GET /applicants/{applicant_id}/applications`

### Documents

- `POST /applications/{application_id}/documents`

### Comments

- `POST /applications/{application_id}/comments`

### Objections

- `POST /applications/{application_id}/objections`

### Timeline

- `GET /applications/{application_id}/timeline`

## Sample MongoDB Documents

### applicants

```json
{
  "id": "app_8bc4f4d3b90c4f9d92e9e4f0c1ab7e13",
  "full_name": "Amina Rahman",
  "national_id": "1998-01-123456",
  "email": "amina@example.com",
  "phone": "+94771234567",
  "address": "12 Galle Road, Colombo",
  "applicant_type": "citizen",
  "verification_state": "unverified",
  "preferred_language": "en",
  "notification_preferences": {
    "email": true,
    "sms": false,
    "in_app": true
  },
  "privacy_settings": {
    "show_contact": false,
    "show_address": false
  },
  "linked_applications": ["app_case_1001"],
  "created_at": "2026-06-20T10:00:00Z",
  "updated_at": "2026-06-20T10:00:00Z"
}
```

### application_documents

```json
{
  "document_id": "doc_92ecbc9d2f2b4c3f94a1b9ab87ff10dd",
  "application_id": "app_case_1001",
  "document_type": "title_deed",
  "file_name": "title_deed.pdf",
  "upload_date": "2026-06-20T10:30:00Z",
  "review_status": "pending",
  "uploaded_by": "app_8bc4f4d3b90c4f9d92e9e4f0c1ab7e13"
}
```

### objections

```json
{
  "objection_id": "obj_4d2cc8f5a6b24d5d9a4a5bfc8e6b7f11",
  "application_id": "app_case_1001",
  "applicant_id": "app_8bc4f4d3b90c4f9d92e9e4f0c1ab7e13",
  "reason": "Boundary dispute raised by neighbor",
  "attachments": ["objection_note.pdf"],
  "status": "submitted",
  "created_at": "2026-06-20T11:00:00Z"
}
```

## Notes

- The profile endpoint can hide sensitive fields with `?include_sensitive=false`.
- Application timelines are assembled from documents, comments, objections, and audit logs.
- MongoDB collections are created automatically on startup.
