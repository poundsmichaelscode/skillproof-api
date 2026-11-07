# SkillProof API — Week 4

Developer: Olayenikan Michael

Focus: Python Backend Engineering
Framework: Django REST Framework

## Goal

Improve the production readiness, reliability,
security and observability of SkillProof API.

## Planned Deliverables

1. Redis cache infrastructure
2. Shared authentication rate limiting
3. Structured application logging
4. Request correlation IDs
5. PostgreSQL backup and recovery
6. Reliability and security regression tests
7. Automated CI verification
8. Final technical documentation

## Existing Baseline

- Django REST Framework
- PostgreSQL 17
- JWT authentication
- Skills, Evidence and Opportunities APIs
- OpenAPI documentation
- Docker and Docker Compose
- GitHub Actions CI
- 114 passing tests at Week 3 completion

## Week 4 Acceptance Criteria

- Redis starts and passes health checks
- Django connects to Redis correctly
- Rate limiting is shared between workers
- Existing API tests continue to pass
- Logging does not expose credentials
- Database backup and restore are demonstrated
- GitHub Actions checks pass
- Week 4 documentation is complete

## Release Strategy

Develop on the week-4 feature branch.

Merge into main only after testing and review.

Create the week-4 tag after final verification.
