# SkillProof API — Week 3 Security Review

## Authentication

The API uses JWT authentication through Django REST
Framework and SimpleJWT.

- Access token lifetime: 15 minutes
- Refresh token lifetime: 7 days
- Authentication header: Authorization: Bearer <token>

## Authentication Rate Limiting

DRF ScopedRateThrottle protects these endpoints:

| Endpoint | Limit |
|---|---|
| Registration | 5 requests/hour |
| JWT login | 10 requests/minute |
| JWT refresh | 20 requests/minute |

When the limit is exceeded, the API returns HTTP 429
using the standard error response format.

## Authorization

Authenticated users can manage their own skills
and evidence. Ownership checks prevent users from
accessing or modifying another user's records.

Opportunity modification is controlled by the
existing owner/admin permission implementation.

## Validation

Input validation includes:

- Password validation during registration
- Uniqueness checks
- Ownership checks on related records
- Field and relationship validation

## Security Testing

- 3 rate-limiting tests passed
- 9 targeted account tests passed
- 114 total automated tests passed

## Production Considerations

Current DRF throttling is an application-level
control, not a complete defense against attacks.

Before production deployment:

1. Configure HTTPS and secure proxy settings.
2. Use a shared cache for throttling across workers.
3. Protect secrets using environment variables.
4. Confirm DEBUG=False and allowed hosts.
5. Configure production static-file handling.
6. Run Django deployment security checks.
7. Add infrastructure-level request rate limiting.
8. Review logging, monitoring, and backup policies.

## Limitations

Rate-limiting tests currently use the development
cache. Production Redis-backed throttling and
distributed load testing remain future deployment
requirements.
