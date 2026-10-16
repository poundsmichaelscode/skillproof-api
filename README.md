# SkillProof API

**A Django REST Framework backend for tracking technical skills, recording evidence of work, and organizing career opportunities.**

> **Status:** Week 1 — Architecture and Core CRUD — completed on 16 October 2026. The `week-1` Git tag preserves the original submission snapshot. This README documents the Week 1 implementation; features planned for later weeks are clearly identified.

## Project overview

SkillProof API helps students, self-taught developers, and early-career professionals organize technical skills in one place. The broader project will also connect skills to evidence such as projects and certifications, and support career opportunity tracking.

The first week's deliverable is a functional Django/PostgreSQL foundation with protected Skill CRUD operations, validation, documentation, and automated tests.

## Week 1 deliverables

- Documented the project idea, three-week plan, database model, ERD, and REST API contract.
- Initialized Django 5.2 and Django REST Framework.
- Configured PostgreSQL 17 through Docker Compose with persistent storage and environment variables.
- Added `GET /api/v1/health/` as a public application-liveness endpoint.
- Implemented a `Skill` model with a user owner, name, description, proficiency, and timestamps.
- Applied `skills.0001_initial` and verified the PostgreSQL schema.
- Enforced case-insensitive uniqueness of skill names per user in PostgreSQL.
- Built the Skill serializer with input validation.
- Implemented authenticated Skill list, create, retrieve, update, and delete operations.
- Restricted Skill queries to the authenticated owner, assigning ownership on the server.
- Passed **25 automated tests** across health checks, models, serializers, CRUD operations, and cross-user restrictions.
- Pushed the annotated **`week-1`** Git tag.

## Technology stack

| Component | Technology |
| --- | --- |
| Language | Python (3.14 used in development) |
| Framework | Django 5.2.18 |
| REST APIs | Django REST Framework 3.18.3 |
| Database | PostgreSQL 17 |
| Driver | psycopg 3 |
| Configuration | `python-dotenv` and `.env` |
| Containers | Docker and Docker Compose |
| Testing | Django test runner and DRF `APIClient` |
| Version control | Git and GitHub |

## Repository structure

```text
skillproof-api/
├── apps/
│   └── skills/
│       ├── migrations/
│       ├── test_api/
│       ├── test_serializers/
│       ├── models.py
│       ├── serializers.py
│       ├── urls.py
│       ├── views.py
│       └── tests.py
├── config/
│   ├── settings.py
│   ├── urls.py
│   ├── views.py
│   └── tests.py
├── docs/
│   ├── idea-one-pager.md
│   ├── work-plan.md
│   ├── data-model.md
│   ├── erd.md
│   ├── api-spec.md
│   └── sample-requests.md
├── .env.example
├── compose.yaml
├── manage.py
└── requirements.txt
```

## Running locally

**Prerequisites:** Git, a compatible Python installation, Docker Desktop (running), and Docker Compose.

### 1. Clone the repository and install dependencies

```bash
git clone https://github.com/poundsmichaelscode/skillproof-api.git
cd skillproof-api
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

### 2. Configure environment variables

```bash
cp .env.example .env
```

Edit `.env` to replace the Django secret and PostgreSQL password placeholders with **new, strong, different** secrets. Do not commit `.env`. To generate a random secret without dollar signs:

```bash
python -c 'import secrets; print(secrets.token_hex(32))'
```

Set `DJANGO_SECRET_KEY` and `POSTGRES_PASSWORD` to separate generated values. The default development configuration uses `skillproof_db`, `skillproof_user`, and PostgreSQL at `127.0.0.1:5433`. The container itself listens on port 5432. If changing credentials after the database volume has been initialized, account for the existing database user/password; environment changes alone do not reset that stored role.

### 3. Start PostgreSQL

```bash
docker compose --env-file .env up -d db
docker compose --env-file .env ps
```

Docker Compose currently starts the **database only**; Django runs on the host.

### 4. Apply migrations and start the API

```bash
python manage.py check
python manage.py migrate
python manage.py runserver 127.0.0.1:8000
```

## Implemented endpoints — Week 1

Base URL: `http://127.0.0.1:8000/api/v1`

| Method | Route | Access | Purpose |
| --- | --- | --- | --- |
| GET | `/health/` | Public | Application liveness check |
| GET | `/skills/` | Authenticated | List the current user's skills |
| POST | `/skills/` | Authenticated | Create a skill |
| GET | `/skills/{id}/` | Authenticated owner | Retrieve an owned skill |
| PUT / PATCH | `/skills/{id}/` | Authenticated owner | Update an owned skill |
| DELETE | `/skills/{id}/` | Authenticated owner | Delete an owned skill |

### Health check

```bash
curl -i http://127.0.0.1:8000/api/v1/health/
```

Expected JSON response:

```json
{"status":"ok"}
```

The health endpoint checks application liveness, not database readiness.

### Example Skill request body

```json
{
  "name": "Python",
  "description": "Backend API development",
  "proficiency": "intermediate"
}
```

Valid proficiency values: `beginner`, `intermediate`, `advanced`. The owner is determined by `request.user`; it cannot be assigned through submitted JSON. Names are trimmed, and duplicate skill names for the same owner are rejected case-insensitively.

**Authentication status:** Week 1 Skill endpoints use DRF `IsAuthenticated`, and tests authenticate users using `APIClient.force_authenticate()`. Public registration and JWT login/refresh endpoints are **not part of the Week 1 release**. See [sample requests](docs/sample-requests.md) for additional request examples and [API specification](docs/api-spec.md) for the **planned** complete API contract.

## Testing

Start PostgreSQL before running database-backed tests, then execute:

```bash
python manage.py check
python manage.py test -v 2
python manage.py makemigrations --check --dry-run
python manage.py migrate --check
```

**Week 1 checkpoint:** 25 tests passed. They cover the health endpoint, Skill model constraints and ownership, serializer validation, Skill CRUD, and cross-user access protection. Django creates a separate temporary test database instead of writing test records into the development database.

## Security implemented so far

- Application and database credentials are read from environment variables.
- The `.env` file must never be committed.
- Skill resources require authentication.
- Skill queries are restricted by user ownership.
- Skill owners are assigned by the server, not accepted from clients.
- PostgreSQL enforces case-insensitive uniqueness per owner.

**Not yet implemented in Week 1:** JWT login, registration, Evidence and Opportunity endpoints, throttling, full OpenAPI documentation, production HTTPS/deployment, and CI. These are covered by later milestones.

## Three-week roadmap

| Week | Focus | Status |
| --- | --- | --- |
| **Week 1** | Architecture, Django/PostgreSQL setup, health check, Skill CRUD and tests | **Completed — `week-1` tag** |
| **Week 2** | User registration, JWT, profile, Evidence, Opportunities, permissions and failure tests | Planned / underway |
| **Week 3** | Expanded tests, OpenAPI/Swagger, CI, production hardening, Dockerized API and final documentation | Planned |

## Project documentation

- [Project overview](docs/idea-one-pager.md)
- [Three-week work plan](docs/work-plan.md)
- [Data model](docs/data-model.md)
- [ERD](docs/erd.md)
- [REST API specification — planned contract](docs/api-spec.md)
- [Sample API requests](docs/sample-requests.md)

## Week 1 submission

- **Repository:** https://github.com/poundsmichaelscode/skillproof-api
- **Week 1 snapshot:** https://github.com/poundsmichaelscode/skillproof-api/tree/week-1
- **Tag:** `week-1`

The `week-1` tag was created before this README; the README is an additional documentation commit on `main`, and the original tagged snapshot remains unchanged.

## Author

**Olayenikan Michael**  
GitHub: https://github.com/poundsmichaelscode

## License

No license has been declared for this repository. Usage and redistribution rights have not been granted through a license file.
