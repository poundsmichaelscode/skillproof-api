# SkillProof API — Week 3 Testing Baseline

## Project
- Track: Backend Development
- Stack: Python, Django REST Framework, PostgreSQL
- Scope: SkillProof API

## Testing approach
The project uses Django's test runner, DRF APIClient,
and a separate PostgreSQL test database.

## Areas covered
- Registration and password hashing
- JWT login, refresh, and rejection cases
- User profile security
- Skill CRUD and ownership
- Evidence CRUD and relationships
- Opportunity CRUD and administrator permissions
- Standardized API errors
- Database validation and cascade deletion

## Coverage limitations
Line coverage does not guarantee security or correctness.
External deployment, reverse-proxy behavior, concurrency,
and production configuration require additional testing.

## Week 3 follow-up
- Review uncovered branches
- Add tests for meaningful edge cases
- Verify 400, 401, 403, 404, and 405 responses
- Add CI execution
- Test containerized deployment

## Measured Coverage

Coverage measured using coverage.py and the Django test runner.

The coverage command is:

```bash
python -m coverage run --source=apps,config \
  --omit="*/migrations/*,*/tests.py,*/test_*.py,*/test_*/test_*.py,*/manage.py" \
  manage.py test -v 1

python -m coverage report -m
```

The latest measured percentage and uncovered lines
are available from the generated coverage report.
