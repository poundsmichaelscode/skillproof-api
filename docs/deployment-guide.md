# SkillProof API — Docker Deployment Guide

## Requirements

- Git
- Docker Engine / Docker Desktop
- Docker Compose

## Environment setup

1. Clone the repository.
2. Copy `.env.example` to `.env`.
3. Generate unique Django and PostgreSQL secrets.
4. Verify that Docker is running.

Never commit `.env`.

## Start the application

```bash
docker compose --env-file .env up -d --build
```

## Apply migrations

```bash
docker compose --env-file .env exec -T api \
  python manage.py migrate
```

## Verify the application

```bash
docker compose --env-file .env ps

curl -i http://127.0.0.1:8002/api/v1/health/

curl -I http://127.0.0.1:8002/api/docs/
```

Expected health response:

```json
{"status":"ok"}
```

## View application logs

```bash
docker compose --env-file .env logs --tail=100 api
```

## Stop services

```bash
docker compose --env-file .env down
```

Do not use `down -v` unless you explicitly intend
to delete the PostgreSQL persistent data volume.

## Architecture

Client
  |
  v
Gunicorn + Django REST Framework
  |
  v
PostgreSQL 17

WhiteNoise serves collected static assets.

## Local Docker networking

- Host API: 127.0.0.1:8002
- Container API: 8000
- Host PostgreSQL: 127.0.0.1:5433
- Container PostgreSQL: db:5432

## Troubleshooting

Check containers:

```bash
docker compose --env-file .env ps
```

Inspect API logs:

```bash
docker compose --env-file .env logs api
```

Check migrations:

```bash
docker compose --env-file .env exec -T api \
  python manage.py migrate --check
```

## Production considerations

This configuration is intended for local verification.

For public production deployment:
- Put the API behind a trusted HTTPS reverse proxy.
- Configure secure proxy and cookie settings.
- Use a shared cache for distributed rate limiting.
- Configure database backups and restoration testing.
- Configure monitoring and log retention.
- Review database exposure and network restrictions.
- Run Django deployment checks.
- Test recovery and rollback procedures.
