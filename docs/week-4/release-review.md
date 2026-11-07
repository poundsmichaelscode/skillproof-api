# SkillProof API — Week 4 Production Readiness Review

## Overview

Week 4 strengthens SkillProof API's operational
reliability, security, observability, and recovery.

The work is implemented on:
`feat/week-4-production-readiness`

## Delivered

### Redis and authentication security
- Shared Redis cache for distributed API throttling.
- Registration, login, and refresh rate limits.
- Controlled HTTP 503 responses if Redis throttling fails.
- Regression tests covering cache failure behavior.

### Observability
- Structured JSON request logs.
- Request correlation identifiers.
- Request duration and HTTP status logging.
- Reduced risk of credentials leaking through access logs.

### PostgreSQL backup and recovery
- Automated PostgreSQL backup script.
- SHA-256 backup integrity verification.
- Isolated restore verification procedure.
- Recovery runbook and operational guidance.

See `docs/week-4/backup-recovery.md`.

### Application health
- `/api/v1/health/` for liveness.
- `/api/v1/health/ready/` for readiness.
- Readiness checks PostgreSQL and Redis.
- HTTP 503 when required dependencies are unavailable.
- Automated failure regression tests.

### Container security
- API runs as a non-root user.
- Application port is bound to localhost in local Compose.
- Docker build excludes environment secrets,
  local virtual environments and backup artifacts.
- PostgreSQL persistent volume remains intact.

## Verification

- Full local suite reached 123 passing tests
  before the four readiness tests were added.
- Readiness checks are covered by the latest
  passing GitHub Actions CI workflow.
- OpenAPI schema generation and validation passed.
- No pending model migrations were detected.
- Hardened Docker image built successfully.
- Image exclusions were verified.
- Running API, PostgreSQL and Redis were healthy.
- Running liveness and readiness endpoints returned HTTP 200.

## Production configuration considerations

- HTTPS termination must be configured at a trusted proxy.
- Production DEBUG must be disabled.
- Production hosts and secret keys must be configured securely.
- Secure cookies and HTTPS redirect must be enabled for HTTPS.
- HSTS subdomain enforcement and preloading require
  deliberate production-domain decisions.
- Configure trusted proxy headers only for a trusted proxy.
- Do not expose PostgreSQL or Redis publicly.
- Verify backup retention, encryption and offsite storage.
- Define and test recovery objectives before production use.
- Add monitoring, alerts and deployment rollback procedures.

## Release decision

Status: Ready for final code review and merge consideration.

This milestone demonstrates local and CI production-readiness
improvements. It does not by itself establish that the application
has been deployed, secured and monitored in a public production
environment.
