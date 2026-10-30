# SkillProof API

A secure, tested Django REST Framework API for managing
technical skills, evidence of practical work, and career
opportunities.

**Developer:** Olayenikan Michael

**Repository:** https://github.com/poundsmichaelscode/skillproof-api

## Project overview

SkillProof helps developers and learners document their
skills, attach evidence of completed work, and organize
career opportunities.

The project was built over three weeks, progressing from
core CRUD functionality to authentication, API security,
documentation, automated testing, and Docker deployment.

## Technology stack

- Python 3.14
- Django 5.2
- Django REST Framework
- PostgreSQL 17
- SimpleJWT
- drf-spectacular (OpenAPI, Swagger, ReDoc)
- Docker and Docker Compose
- Gunicorn
- WhiteNoise
- GitHub Actions

## Features

### Authentication
- User registration
- JWT access and refresh tokens
- User profile retrieval and update
- Password validation
- Authentication rate limiting

### Skills
- Create, list, retrieve, update, and delete skills
- Per-user ownership enforcement
- Case-insensitive skill-name uniqueness
- Proficiency tracking

### Evidence
- Create and manage skill evidence
- Associate evidence with owned skills
- Owner-filtered access

### Opportunities
- Create and manage career opportunities
- Authenticated listing
- Owner/admin modification permissions

### API reliability
- Standardized error responses
- Page-number pagination
- PostgreSQL query indexes
- OpenAPI schema and interactive documentation
- Automated tests and GitHub Actions CI

## Quick start with Docker

Requirements:
- Docker Desktop or Docker Engine with Compose
- Git

Clone the repository:

```bash
git clone https://github.com/poundsmichaelscode/skillproof-api.git
cd skillproof-api
cp .env.example .env
```

Replace the placeholder secrets in .env with unique,
strong values before starting the containers.

Start PostgreSQL and the Django API:

```bash
docker compose --env-file .env up -d --build
```

Apply database migrations:

```bash
docker compose --env-file .env exec -T api \
  python manage.py migrate
```

Check container status:

```bash
docker compose --env-file .env ps
```

The local API is available at:

http://127.0.0.1:8002

## API endpoints

| Method | Endpoint | Purpose |
| --- | --- | --- |
| GET | /api/v1/health/ | Public health check |
| POST | /api/v1/auth/register/ | Register user |
| POST | /api/v1/auth/token/ | Obtain JWT tokens |
| POST | /api/v1/auth/token/refresh/ | Refresh token |
| GET, PATCH | /api/v1/auth/me/ | Current user profile |
| GET, POST | /api/v1/skills/ | List or create skills |
| GET, PUT, PATCH, DELETE | /api/v1/skills/{id}/ | Manage a skill |
| GET, POST | /api/v1/evidence/ | List or create evidence |
| GET, PUT, PATCH, DELETE | /api/v1/evidence/{id}/ | Manage evidence |
| GET, POST | /api/v1/opportunities/ | List or create opportunities |
| GET, PUT, PATCH, DELETE | /api/v1/opportunities/{id}/ | Manage opportunity |

## API documentation

- OpenAPI: /api/schema/
- Swagger UI: /api/docs/
- ReDoc: /api/redoc/

Local Swagger URL:

http://127.0.0.1:8002/api/docs/

## Pagination

List endpoints support:

- page
- page_size

Default page size: 20
Maximum page size: 100

## Authentication rate limits

| Endpoint | Limit |
| --- | --- |
| Registration | 5/hour |
| Login | 10/minute |
| Token refresh | 20/minute |

Requests exceeding configured limits receive HTTP 429.

## Testing

Run locally after activating the Python environment:

```bash
python manage.py check
python manage.py test -v 1
python manage.py makemigrations --check --dry-run
python manage.py spectacular \
  --validate --fail-on-warn \
  --file /tmp/skillproof-openapi.yaml
```

Latest verified local result: 114 tests passed.

GitHub Actions runs the tests with PostgreSQL, validates
migrations and OpenAPI, and builds the Docker image.

## Project milestones

| Week | Deliverable | Status |
| --- | --- | --- |
| 1 | Architecture, PostgreSQL, Skill CRUD | Complete |
| 2 | JWT, relationships, permissions, error handling | Complete |
| 3 | Tests, API docs, performance, Docker, CI | Complete |

Historical Git tags:
- week-1
- week-2
- week-2-final

The week-3 tag is created after final verification.

## Deployment limitations

The project has been verified using local Docker Compose.
It has not been demonstrated as a publicly hosted service.

Before public production deployment, configure HTTPS,
a trusted reverse proxy, a shared throttling cache,
monitoring, backups, and additional security testing.

## Documentation

- [Work plan](docs/work-plan.md)
- [Data model](docs/data-model.md)
- [ERD](docs/erd.md)
- [API specification](docs/api-spec.md)
- [Performance review](docs/week-3-performance.md)
- [Security review](docs/week-3-security.md)
- [Week 3 submission](docs/week-3-submission.md)
- [Deployment guide](docs/deployment-guide.md)
- [Technical reflection](docs/technical-reflection.md)

## AI disclosure

AI tools assisted with planning, coding suggestions,
troubleshooting, and documentation.

Implementation was validated through local testing,
Docker execution, and GitHub Actions.

## Author

Olayenikan Michael
GitHub: https://github.com/poundsmichaelscode

## License

No license has been declared for this repository.
