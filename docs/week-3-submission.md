# SkillProof API — Week 3 Submission

## Project
SkillProof API

## Developer
Olayenikan Michael

## Repository
https://github.com/poundsmichaelscode/skillproof-api

## Technology
Python, Django REST Framework, PostgreSQL 17,
JWT, Docker, Gunicorn, WhiteNoise, GitHub Actions.

## Completed Features
- User registration and JWT authentication
- User profile retrieval and update
- Owner-protected Skill CRUD
- Owner-protected Evidence CRUD
- Opportunity management with authorization
- Consistent API error responses
- OpenAPI schema, Swagger UI and ReDoc
- Page-number pagination
- Database indexes for common queries
- Authentication endpoint rate limiting
- Dockerized Django and PostgreSQL
- Non-root application container
- Static file delivery using WhiteNoise
- Automated GitHub Actions CI

## Testing
114 automated Django tests passed locally.

GitHub Actions:
- Run #1: successful
- Run #2: successful

## Local Docker Verification
- PostgreSQL container healthy
- Gunicorn application served HTTP 200
- Health endpoint returned HTTP 200
- OpenAPI schema returned HTTP 200
- Swagger JavaScript returned HTTP 200

## Production Limitations
The Docker deployment is verified locally but is
not yet a public production deployment.

Before public deployment:
- Configure a trusted HTTPS reverse proxy
- Use a shared cache for distributed rate limiting
- Verify secure headers, cookies and proxy settings
- Configure monitoring and backups
- Conduct production load and security testing

## AI Assistance Disclosure
AI assistance was used to help plan implementation
steps, generate initial code suggestions, explain
errors, and develop test and documentation examples.

Implementation was verified through local commands,
automated tests, Docker checks and GitHub Actions.
