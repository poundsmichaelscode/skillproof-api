# SkillProof API — Week 2 Issue and Decision Log

This log distinguishes risks observed in code review from bugs reproduced during development. Do not describe open risks as fixed bugs.

| ID | Type | Finding and evidence | Mitigation/decision | Status |
| --- | --- | --- | --- | --- |
| SEC-01 | Risk | Email is checked with `email__iexact` but Django's default User table lacks a unique email constraint | Defer migration strategy, document concurrency exposure | Open |
| SEC-02 | Risk | Auth token/registration endpoints lack dedicated throttling | Schedule throttling plus edge limit in Week 3 | Open |
| SEC-03 | Risk | Seven-day refresh token without rotation/revocation | Assess blacklist and logout semantics in Week 3 | Open |
| SEC-04 | Authorization policy | `is_staff` authorizes any Opportunity edit/delete | Explicitly document MVP policy; revisit model permissions for production | Accepted for MVP |
| SEC-05 | Data integrity | Django model `full_clean` is bypassed by bulk SQL/ORM updates | Restrict bulk mutation and document need for DB integrity strategy | Open |
| SEC-06 | Contract mismatch | DRF's native error responses did not match documented API error envelope | Add centralized exception handler and tests | Resolved once final test run passes |
| DOC-01 | Documentation drift | API specification claimed no endpoints implemented and Week 1 sample requests said JWT was future work | Update API status and Week 2 request examples | Resolved once docs are merged |

## Week 1 mentor feedback response

No actual mentor feedback text was supplied. **Do not invent feedback.** Enter each real feedback item here when available:

| Feedback received | Action taken / reason deferred | Evidence link |
| --- | --- | --- |
| Not provided yet | Pending mentor feedback | — |

## Key delivery decisions

- Preserve the built-in Django User model and existing migrations.
- Keep skills and evidence owner-private, while opportunities are browsable by authenticated users.
- Preserve established HTTP status codes while unifying DRF-handled error response bodies.
- Maintain one public repository, small verified commits, and a weekly tag.

## AI / source declaration

Development used ChatGPT for implementation suggestions, test scaffolding, review, and documentation drafting. The developer ran the code and tests locally, reviewed outputs, and committed the changes. Project requirements are based on the provided BuildLab Stage 1 Work Guide. Replace this note if the actual assistance used differs.
