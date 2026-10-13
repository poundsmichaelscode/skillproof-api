# SkillProof API — Three-Week Work Plan

## Project Goal

Build a secure, tested, documented, and deployable
Django REST Framework API within three weeks.

## Week 1 — Architecture and Core CRUD

Goal: Establish the project foundation and implement
the first working resource.

Tasks:
- Audit and plan the repository.
- Document the project idea and requirements.
- Design database entities and relationships.
- Create an Entity Relationship Diagram (ERD).
- Define the REST API specification.
- Initialize Django and Django REST Framework.
- Configure PostgreSQL and environment variables.
- Implement a health-check endpoint.
- Implement skill CRUD endpoints.
- Add basic validation and sample requests.

Acceptance Criteria:
- Project runs locally.
- Database migrations succeed.
- Architecture and API specification exist.
- Skill CRUD endpoints work.
- Basic endpoint verification passes.
- Week 1 changes are committed.
- The week-1 tag is pushed.

## Week 2 — Authentication and Relationships

Goal: Secure the API and implement related resources.

Tasks:
- Implement user registration.
- Implement JWT login.
- Add user profile endpoints.
- Enforce authentication and ownership permissions.
- Implement evidence endpoints.
- Implement career opportunity endpoints.
- Validate relationships and incoming requests.
- Standardize error handling.
- Test authentication and authorization failures.
- Document at least five genuine bugs or risks.

Acceptance Criteria:
- Authentication works.
- Passwords are hashed.
- Private resources require authentication.
- Cross-user access is prevented.
- Related resources work correctly.
- Important failure cases are tested.
- The week-2 tag is pushed.

## Week 3 — Testing and Deployment

Goal: Deliver a reliable, documented backend API.

Tasks:
- Complete unit and integration tests.
- Configure OpenAPI and Swagger documentation.
- Review security and performance.
- Configure pagination and relevant indexes.
- Add Docker and Docker Compose.
- Configure GitHub Actions CI.
- Prepare production environment configuration.
- Deploy the API where resources permit.
- Verify deployment or local Docker execution.
- Complete README and technical case study.
- Prepare walkthrough and technical reflection.
- Declare AI assistance and external libraries.

Acceptance Criteria:
- Automated tests pass.
- API documentation works.
- Docker setup works locally.
- GitHub Actions checks pass.
- Security notes are documented.
- Deployment or local run guide is available.
- Final submission materials are complete.
- The week-3 tag is pushed.

## Top Three Project Risks

### Risk 1 — Scope Creep
Impact: Too many features may delay completion.

Mitigation:
Focus on authentication, skills, evidence,
and opportunities. Defer nonessential features.

### Risk 2 — Database Configuration
Impact: PostgreSQL connection or migration errors
may block development.

Mitigation:
Use environment variables, small migrations,
and early database connection checks.

### Risk 3 — Authorization Vulnerabilities
Impact: Users could access or modify records
belonging to other users.

Mitigation:
Use DRF permissions, ownership-filtered querysets,
and automated cross-user access tests.

## Development Workflow

1. Implement one small milestone at a time.
2. Run relevant tests and validation checks.
3. Review changes and check for secrets.
4. Commit each verified milestone separately.
5. Push completed work to GitHub.
6. Create weekly tags only after acceptance
   criteria are satisfied.

## Definition of Done

A milestone is complete only after its deliverables
exist, verification passes, and its Git commit is
confirmed.
