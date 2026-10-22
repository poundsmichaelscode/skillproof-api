# SkillProof API — Week 2 Security Review

## Review Scope

This review covers the Week 2 implementation of:

- User registration and JWT authentication
- User profile management
- Skill ownership permissions
- Evidence ownership and skill relationships
- Career Opportunity permissions

The full automated test suite passed 99 tests at the
Week 2 Opportunity CRUD checkpoint.

This is an implementation review, not a penetration test.

## Verified Security Controls

1. Passwords are hashed using Django's create_user().
2. Protected API endpoints require authentication.
3. JWT access tokens are checked by Simple JWT.
4. Skill queries are restricted by authenticated owner.
5. Evidence references are limited to owned skills.
6. Opportunity modifications require ownership or staff access.
7. User profile updates exclude password and privilege fields.
8. Cross-user access restrictions have automated tests.

## Findings and Risks

### SEC-01 — Email Uniqueness Race Condition

Severity: Medium

Location:
apps/accounts/serializers.py

Observation:
Registration and profile updates check whether an email
already exists using a database query.

Risk:
Concurrent requests can pass these checks before either
transaction commits because Django's default User.email
does not have a database-level uniqueness constraint.

Recommendation:
Introduce database-enforced case-insensitive email
uniqueness after evaluating existing user records,
or adopt a suitable custom user design for a future version.

Status: Open.

### SEC-02 — Missing Authentication Throttling

Severity: High

Locations:
apps/accounts/urls.py
config/settings.py

Observation:
No authentication-specific request throttling is
configured for the registration or JWT login endpoints.

Risk:
Automated password guessing and account creation abuse
may be easier.

Recommendation:
Introduce request throttling at the application layer,
alongside reverse-proxy or edge rate limiting.
Test rate-limit responses and proxy IP handling.

Status: Open.

### SEC-03 — Refresh Token Revocation

Severity: Medium

Location:
config/settings.py

Observation:
JWT refresh tokens have a seven-day lifetime.
Token rotation is disabled, and no blacklist/revocation
system is configured.

Risk:
A stolen refresh token may remain usable until it expires
unless account or signing-key controls invalidate it.

Recommendation:
Evaluate refresh-token rotation, blacklisting, token
revocation on logout, and secure token storage.

Status: Open.

### SEC-04 — Broad Staff Permissions

Severity: Medium

Location:
apps/opportunities/permissions.py

Observation:
All authenticated users with is_staff=True can update
or delete opportunities belonging to other users.

Risk:
This may grant broader permissions than intended if the
application later introduces multiple staff roles.

Recommendation:
Replace the generic staff check with an explicit
Django model permission or application-specific role
when administrator responsibilities are finalized.

Status: Open — current behavior matches the MVP policy.

### SEC-05 — Model Validation Can Be Bypassed

Severity: Medium

Location:
apps/evidence/models.py

Observation:
Evidence ownership consistency is checked during
model cleaning and normal save() operations.

Risk:
Bulk updates, bulk creation, and direct SQL may bypass
this Python-level validation.

Recommendation:
Continue validating owner/skill relationships in DRF,
restrict bulk writes, and assess database-level protections
if bulk operations are introduced.

Status: Open.

### SEC-06 — Inconsistent API Error Formatting

Severity: Low

Locations:
apps/accounts/
apps/skills/
apps/evidence/
apps/opportunities/

Observation:
The planned API specification defines a consistent
error object, but the current application largely uses
default Django REST Framework error responses.

Risk:
Client applications must handle multiple error formats.

Recommendation:
Implement and test a centralized DRF exception handler.

Status: Open.

## Week 3 Hardening Backlog

- Implement authentication throttling.
- Add standardized API error responses.
- Evaluate refresh-token revocation.
- Review the email uniqueness strategy.
- Add pagination and relevant query indexes.
- Run Django deployment security checks.
- Introduce HTTPS and production environment settings.
- Configure automated CI checks.

## Conclusion

The MVP has functional authentication and authorization
tests. The issues above are tracked implementation
risks requiring follow-up before production deployment.

No claim of production security certification is made.
