# SkillProof API — Technical Reflection

## Overview

SkillProof API was developed as a three-week backend
engineering project using Django REST Framework
and PostgreSQL.

## Week 1 — Foundation

I established the application architecture, database
models, REST API contract, and initial Skill CRUD
implementation.

This phase reinforced the importance of data modeling,
validation, and incremental testing.

## Week 2 — Security and relationships

I implemented user registration, JWT authentication,
profile management, Evidence and Opportunity resources,
and ownership-based authorization.

The most important lesson was that authenticating a
request is not sufficient: each resource also needs
appropriate authorization checks.

## Week 3 — Reliability and deployment

I extended the automated test suite, introduced API
documentation, added pagination and database indexes,
implemented authentication throttling, and containerized
the application.

I also configured GitHub Actions to run tests and
validate the Docker build.

## Challenges and solutions

### Database configuration

PostgreSQL required correct connection settings for
host-based development and Docker networking.

I used environment variables to separate those
configurations.

### Pagination compatibility

Introducing pagination changed the response structure
of list endpoints.

I updated existing tests to verify the results field
inside the paginated response.

### Static files

Swagger assets needed explicit static-file handling
when Django DEBUG was disabled.

I configured WhiteNoise and collectstatic.

### CI runner scheduling

GitHub Actions initially remained queued.
The workflows subsequently executed successfully.

## Testing and verification

- 114 automated tests passed locally.
- OpenAPI validation completed without warnings.
- Docker health checks returned HTTP 200.
- GitHub Actions runs #1 and #2 passed.

## Remaining improvements

The application is locally deployable, but additional
work remains for a public production environment,
including HTTPS, shared throttling storage,
monitoring, backup testing, and load testing.

## AI assistance disclosure

AI tools supported implementation planning, code
examples, troubleshooting, and documentation drafting.

The proposed changes were validated using terminal
commands, automated tests, Docker, and GitHub Actions.
