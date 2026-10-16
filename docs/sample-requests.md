# SkillProof API — Example Requests

Base URL: http://127.0.0.1:8000/api/v1

## Health check

GET /health/

Expected response: 200 OK

```json
{"status": "ok"}
```

## Skill endpoints

Skill endpoints require an authenticated user.

JWT authentication will be implemented in Week 2.
At present, the API supports Django/DRF session
authentication, and authenticated requests are
verified using automated DRF APIClient tests.

### Create skill

POST /skills/

```json
{
  "name": "Python",
  "description": "Backend development",
  "proficiency": "intermediate"
}
```

Expected status: 201 Created.

The owner is assigned from the authenticated user.

### List skills

GET /skills/

Expected status: 200 OK.

Only skills belonging to the authenticated user
are returned.

### Retrieve skill

GET /skills/1/

Expected status: 200 OK for an owned record.

### Update skill

PATCH /skills/1/

```json
{
  "proficiency": "advanced"
}
```

Expected status: 200 OK.

### Delete skill

DELETE /skills/1/

Expected status: 204 No Content.

## Security expectations

- Anonymous users cannot access skill endpoints.
- Users cannot assign another owner to a skill.
- Users cannot access another user's skill records.
- Duplicate skill names for the same owner are rejected.
- A different user may register the same skill name.

## Verification

Run:

```bash
python manage.py check
python manage.py test -v 2
python manage.py makemigrations --check --dry-run
```

Actual CRUD responses and access restrictions are
covered by apps/skills/test_api/test_skill_api.py.
