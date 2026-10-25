# Week 2 — Backend Development — SkillProof API

**Track:** Backend Development  
**Repository:** https://github.com/poundsmichaelscode/skillproof-api  
**Tag:** `week-2` (create only after all final checks pass)  
**Run guide:** repository `README.md` (local Django and PostgreSQL Compose setup)

## Delivered

- Registration with Django password hashing, JWT obtain/refresh, and protected profile endpoints.
- Skill JWT ownership regression tests.
- Evidence model, Skill relationship, validation, private CRUD, and owner-only access tests.
- Opportunity model, authenticated listing, CRUD, and creator/staff modification rules.
- Consistent error envelope for handled DRF API errors, with regression tests.
- Updated Mermaid ERD, request-flow architecture, example API requests, and issue/security logs.

## Feedback response

No specific Week 1 mentor comments have been provided. Feedback tracking is prepared in `docs/week-2-issue-log.md`; do not imply mentor feedback was received.

## Technical decisions

- PostgreSQL foreign keys with cascades; authenticated owner filtering for sensitive data.
- JWT Bearer authentication for client API requests.
- Safe generic authentication and authorization error messages while preserving useful 400 field-validation details.
- No secrets, real passwords, or personal production data stored in the repository.

## Known blockers and risks

See `docs/week-2-security-review.md` and `docs/week-2-issue-log.md`. The main outstanding production hardening items are auth rate limiting, refresh-token revocation, email uniqueness at database level, stronger admin roles, and monitoring/CI.

## Verification and submission

Run `python manage.py check`, `python manage.py test -v 1`, and `python manage.py makemigrations --check --dry-run`. Record the final passing test count, push commits, create/push `week-2`, and submit the repository, tag, local run guide, and this weekly note through the official form.
