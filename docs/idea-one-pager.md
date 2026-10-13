# SkillProof API — Project One-Pager

## Project Overview

SkillProof API is a backend REST API built with Python,
Django, and Django REST Framework.

It helps learners track their technical skills, attach
evidence of completed work, and manage career opportunities.

## Problem Statement

Students and early-career developers often have their skills,
projects, certifications, and learning achievements scattered
across different platforms.

SkillProof provides a centralized system for organizing
these records through a secure REST API.

## Target Users

- Students learning software development
- Self-taught developers
- Early-career technology professionals
- Learners building technical portfolios

## MVP Features

### User Accounts
- User registration
- JWT authentication
- Profile retrieval and updates

### Skills
- Create, read, update, and delete skills
- Associate skills with authenticated users
- Protect private user records

### Evidence
- Record projects, certifications, and achievements
- Attach evidence URLs to skills
- Enforce ownership permissions

### Career Opportunities
- Create and browse opportunities
- Store organization and application details
- Restrict modification to authorized users

## Technology Stack

- Python
- Django
- Django REST Framework
- PostgreSQL
- Django ORM
- JWT Authentication
- pytest and pytest-django
- Docker and Docker Compose
- GitHub Actions
- drf-spectacular

## Out of Scope

- AI recommendations
- Payment processing
- Real-time messaging
- File uploads
- Complex third-party integrations

## Success Criteria

The project will be considered successful when:

1. The REST API supports the required CRUD operations.
2. Authentication and authorization work correctly.
3. Database relationships are implemented and validated.
4. Automated tests cover critical functionality.
5. OpenAPI documentation is available.
6. Docker-based execution works locally.
7. GitHub Actions runs automated checks.
8. Deployment or a reliable local run guide is available.

## Delivery Timeline

Three weeks.

Week 1: Architecture, database design, and core CRUD.

Week 2: Authentication, relationships, and validation.

Week 3: Testing, documentation, security, and deployment.
