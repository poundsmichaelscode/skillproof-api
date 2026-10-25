# Week 2 API requests — dummy data only

Start PostgreSQL and Django using the repository README. Base URL: `http://127.0.0.1:8000/api/v1`.

## Create account

```bash
curl -i -X POST http://127.0.0.1:8000/api/v1/auth/register/ \
  -H 'Content-Type: application/json' \
  -d '{"username":"demo_learner","email":"demo_learner@example.com","password":"DemoOnlyStrong#7421","password_confirm":"DemoOnlyStrong#7421"}'
```

## Login and refresh

```bash
curl -i -X POST http://127.0.0.1:8000/api/v1/auth/token/ \
  -H 'Content-Type: application/json' \
  -d '{"username":"demo_learner","password":"DemoOnlyStrong#7421"}'
```

Copy the `access` value from the response into a shell variable (do not echo, share, or commit real tokens):

```bash
read -r -s ACCESS_TOKEN
# Paste access token and press Return
curl -i http://127.0.0.1:8000/api/v1/auth/me/ \
  -H "Authorization: Bearer $ACCESS_TOKEN"
```

Refresh with `POST /api/v1/auth/token/refresh/` and `{"refresh":"<refresh token>"}`; do not publish a real token.

## Create related records

```bash
curl -i -X POST http://127.0.0.1:8000/api/v1/skills/ \
  -H "Authorization: Bearer $ACCESS_TOKEN" -H 'Content-Type: application/json' \
  -d '{"name":"Python","description":"Backend APIs","proficiency":"intermediate"}'
```

Use the `id` of the created Skill in the Evidence request:

```bash
curl -i -X POST http://127.0.0.1:8000/api/v1/evidence/ \
  -H "Authorization: Bearer $ACCESS_TOKEN" -H 'Content-Type: application/json' \
  -d '{"skill":1,"title":"Python REST API","evidence_url":"https://example.com/demo"}'
```

```bash
curl -i -X POST http://127.0.0.1:8000/api/v1/opportunities/ \
  -H "Authorization: Bearer $ACCESS_TOKEN" -H 'Content-Type: application/json' \
  -d '{"title":"Junior Backend Developer","organization":"Demo Co","application_url":"https://example.com/jobs/123"}'
```

List resources using `GET /api/v1/skills/`, `/api/v1/evidence/`, and `/api/v1/opportunities/` with the same Bearer header. Updates use `PATCH /api/v1/<resource>/<id>/`, deletions use `DELETE`.

## Errors to demonstrate

Without a token, protected routes return `401`. When an authenticated user changes another user's Opportunity, the response is `403`. Private Skill/Evidence records not owned by the caller return `404`. Invalid inputs return `400`, for example:

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid request data.",
    "details": {"title": ["This field is required."]}
  }
}
```

Status codes stay unchanged; details reflect actual validation failures. Replace any example IDs with IDs from your local dummy records.
