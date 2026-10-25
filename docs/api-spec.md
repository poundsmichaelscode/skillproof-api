# SkillProof API — REST API Specification

## 1. Overview

SkillProof API provides REST endpoints for managing
users, skills, evidence, and career opportunities.

API base path: /api/v1/

Content type: application/json

Authentication: JWT Bearer token

All deployed API traffic must use HTTPS.

## 2. Authentication

### POST /api/v1/auth/register/

Public endpoint.

Request:
{
  "username": "learner1",
  "email": "learner@example.com",
  "password": "StrongPassword123!",
  "password_confirm": "StrongPassword123!"
}

Success: 201 Created

Response:
{
  "id": 1,
  "username": "learner1",
  "email": "learner@example.com"
}

Password is hashed and never returned.

### POST /api/v1/auth/token/

Public endpoint.

Request:
{
  "username": "learner1",
  "password": "StrongPassword123!"
}

Success: 200 OK

Response:
{
  "access": "<jwt-access-token>",
  "refresh": "<jwt-refresh-token>"
}

Invalid credentials: 401 Unauthorized.

### POST /api/v1/auth/token/refresh/

Public endpoint accepting a valid refresh token.

Request:
{
  "refresh": "<jwt-refresh-token>"
}

Success: 200 OK

Response:
{
  "access": "<new-jwt-access-token>"
}

Invalid or expired refresh token: 401.

### GET /api/v1/auth/me/

Requires authentication.

Returns authenticated user information.

Success: 200 OK

### PATCH /api/v1/auth/me/

Requires authentication.

Updates permitted profile fields only.

Password and administrator privileges cannot
be modified through this endpoint.

## 3. Skills

### GET /api/v1/skills/

Requires authentication.

Returns the authenticated user's skills.

Pagination is planned for Week 3.

Query parameters:
- page
- page_size

### POST /api/v1/skills/

Requires authentication.

Request:
{
  "name": "Python",
  "description": "Backend development",
  "proficiency": "beginner"
}

Success: 201 Created

The owner is assigned from request.user.

### GET /api/v1/skills/{id}/

Requires authentication.

Returns an owned skill.

Success: 200 OK
Not found or not owned: 404 Not Found

### PATCH /api/v1/skills/{id}/

Requires authentication and ownership.

Updates allowed skill fields.

Success: 200 OK

### DELETE /api/v1/skills/{id}/

Requires authentication and ownership.

Success: 204 No Content

Deleting a skill also deletes its evidence.

## 4. Evidence

### GET /api/v1/evidence/

Requires authentication.

Lists only the authenticated user's evidence.

Pagination and skill filtering are planned for Week 3.

### POST /api/v1/evidence/

Requires authentication.

Request:
{
  "skill": 1,
  "title": "Python REST API Project",
  "description": "Built a Django API",
  "evidence_url": "https://github.com/example/project"
}

Success: 201 Created

The referenced skill must belong to request.user.

The owner is assigned server-side.

### GET /api/v1/evidence/{id}/

Returns an owned evidence record.

Success: 200 OK

### PATCH /api/v1/evidence/{id}/

Updates an owned evidence record.

Changing its skill requires ownership validation.

### DELETE /api/v1/evidence/{id}/

Deletes an owned evidence record.

Success: 204 No Content

## 5. Career Opportunities

### GET /api/v1/opportunities/

Requires authentication.

All authenticated users can browse opportunities.

Pagination is planned for Week 3.

### POST /api/v1/opportunities/

Requires authentication.

Request:
{
  "title": "Junior Backend Developer",
  "organization": "Example Technologies",
  "description": "Backend engineering opportunity",
  "application_url": "https://example.com/jobs/1",
  "closing_date": "2026-12-31"
}

Success: 201 Created

Owner is assigned server-side.

### GET /api/v1/opportunities/{id}/

Requires authentication.

Returns an opportunity.

Success: 200 OK

### PATCH /api/v1/opportunities/{id}/

Requires authentication.

Only the owner or authorized administrator
can update the opportunity.

### DELETE /api/v1/opportunities/{id}/

Requires authentication.

Only the owner or authorized administrator
can delete the opportunity.

Success: 204 No Content

## 6. Health Check

### GET /api/v1/health/

Public endpoint.

Success: 200 OK

Response:
{
  "status": "ok"
}

This is an application liveness check.
Database readiness is a separate concern.

## 7. Validation Rules

- Skill names cannot be empty.
- Proficiency must be beginner, intermediate,
  or advanced.
- Skill names must be unique per user after
  normalization.
- Evidence titles cannot be empty.
- Evidence URLs must be valid.
- Evidence skills must belong to the owner.
- Opportunity titles are required.
- Organization names are required.
- Application URLs must be valid.
- Closing dates must be valid ISO dates.
- Clients cannot set owner fields.

## 8. Authentication and Authorization

Protected endpoints require:

Authorization: Bearer <access-token>

Private records are filtered by request.user.

Owners cannot modify other users' records.

Administrators may manage opportunities
according to their assigned permissions.

## 9. HTTP Status Codes

200 OK: Successful retrieval or update.

201 Created: Resource created.

204 No Content: Resource deleted.

400 Bad Request: Invalid request data.

401 Unauthorized: Missing or invalid credentials.

403 Forbidden: Authenticated but insufficient
permission to perform the operation.

404 Not Found: Missing or inaccessible resource.

405 Method Not Allowed: Unsupported HTTP method.

429 Too Many Requests: Request throttled.

500 Internal Server Error: Unexpected server failure (handled by Django outside the DRF exception handler).

## 10. Error Response Format

Application errors will use a consistent format.

Example:
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid request data.",
    "details": {
      "name": ["This field is required."]
    }
  }
}

Possible codes:
- VALIDATION_ERROR
- AUTHENTICATION_FAILED
- PERMISSION_DENIED
- NOT_FOUND
- RATE_LIMITED
- INTERNAL_ERROR

Error details are optional.

Internal stack traces must never be returned
in production responses.

## 11. Pagination

Planned default page size: 20 (not enabled in Week 2)

Planned maximum page size: 100 (not enabled in Week 2)

Example:
GET /api/v1/skills/?page=1&page_size=20

Response:
{
  "count": 1,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "name": "Python",
      "proficiency": "beginner"
    }
  ]
}

## 12. Security Requirements

- Store credentials and keys in environment variables.
- Use Django's built-in password hashing.
- Validate and sanitize inputs as appropriate.
- Enforce object ownership.
- Configure authentication throttling.
- Never expose password hashes or JWT secrets.
- Restrict allowed hosts in production.
- Use HTTPS in production.

## 13. Implementation Status

This document defines the planned API contract.

Week 2 implementation includes registration, JWT obtain/refresh, user profile,
Skill CRUD, Evidence CRUD, Opportunity CRUD, and health check.

The standardized DRF-handled API error envelope is implemented in
`config/exceptions.py`. Authentication and permissions are covered by
regression tests. The current API has **no global pagination configuration**,
so list endpoints return plain arrays; pagination, filtering, throttling,
and production hardening are planned for Week 3.

The pagination section above represents the **planned Week 3 contract**,
not currently active behavior. See `docs/sample-requests.md` for examples.
