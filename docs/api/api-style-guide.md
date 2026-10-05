# API Style Guide

All 10 projects follow this API design contract. Deviations require a documented ADR and human approval.

## URL Structure

```
https://<host>/v1/<resource>[/<id>][/<sub-resource>]
```

All routes are versioned under `/v1/`. Trailing slashes are not used.

**Examples:**
```
GET  /v1/documents
POST /v1/documents
GET  /v1/documents/{id}
POST /v1/documents/{id}/chunks
GET  /v1/health
GET  /v1/ready
```

## HTTP Method Semantics

| Method | Use |
|---|---|
| GET | Read a resource or collection |
| POST | Create a resource or trigger an action |
| PUT | Replace a resource (full update) |
| PATCH | Partial update |
| DELETE | Remove a resource |

## Request Format

- Content-Type: `application/json`
- All request bodies are validated against a Pydantic schema
- Required fields missing → 422
- Unknown fields → ignored (not 422, to allow forward compatibility)

## Response Format

### Success

```json
{
  "data": { ... },
  "meta": {
    "request_id": "req_abc123",
    "timestamp": "2026-10-05T12:00:00Z"
  }
}
```

For collections:
```json
{
  "data": [ ... ],
  "meta": {
    "request_id": "req_abc123",
    "timestamp": "2026-10-05T12:00:00Z",
    "pagination": {
      "page": 1,
      "page_size": 25,
      "total": 150,
      "has_next": true
    }
  }
}
```

### Error

```json
{
  "error": {
    "code": "DOCUMENT_NOT_FOUND",
    "message": "No document with ID doc_xyz789 exists in this workspace.",
    "request_id": "req_abc123",
    "details": []
  }
}
```

For validation errors (422):
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Request validation failed.",
    "request_id": "req_abc123",
    "details": [
      { "field": "title", "message": "Field required." },
      { "field": "file_size_bytes", "message": "Must be a positive integer." }
    ]
  }
}
```

## HTTP Status Codes

| Code | Meaning |
|---|---|
| 200 | Success (GET, PATCH, PUT) |
| 201 | Created (POST that creates a resource) |
| 202 | Accepted (async operations started) |
| 204 | No Content (DELETE) |
| 400 | Bad Request (malformed, unparseable) |
| 401 | Unauthenticated (missing or invalid token) |
| 403 | Forbidden (authenticated but not authorized) |
| 404 | Not Found |
| 409 | Conflict (duplicate, state mismatch) |
| 422 | Validation Error (parseable but semantically invalid) |
| 429 | Rate Limited |
| 500 | Internal Server Error |
| 503 | Service Unavailable (dependency down) |

## Authentication

All protected endpoints require one of:
- `Authorization: Bearer <jwt_token>` — for user sessions
- `X-API-Key: <api_key>` — for service-to-service

Unauthenticated requests return 401 with no hint about credential validity.

## Pagination

Offset-based pagination (default):
```
GET /v1/documents?page=2&page_size=25
```

Cursor-based pagination (for large/real-time datasets):
```
GET /v1/traces?cursor=<opaque_cursor>&limit=50
```

Default page size: 25. Maximum page size: 100.

## Rate Limiting Headers

Every response includes:
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 42
X-RateLimit-Reset: 1728129600
```

Rate-limited responses: 429 with `Retry-After` header.

## Async Operations

Long-running operations return 202 with a job reference:
```json
{
  "data": {
    "job_id": "job_abc123",
    "status": "pending",
    "status_url": "/v1/jobs/job_abc123"
  }
}
```

Job status polling:
```
GET /v1/jobs/{job_id}
→ { "data": { "job_id": "...", "status": "running|completed|failed", "result": {...} } }
```

## Health Endpoints

```
GET /health  → 200 { "status": "ok" }  (liveness — process is alive)
GET /ready   → 200 { "status": "ready", "checks": { "db": "ok", "redis": "ok" } }
             → 503 { "status": "degraded", "checks": { "db": "error", "redis": "ok" } }
```

## OpenAPI Documentation

Every project auto-generates OpenAPI 3.1 docs at `/docs` (Swagger UI) and `/openapi.json`. The `openapi.yaml` in `docs/api/` is the source of truth for contract testing.
