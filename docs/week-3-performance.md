# SkillProof API — Week 3 Performance Review

## Pagination

Skills, Evidence, and Opportunities use DRF page-number
pagination.

- Default page size: 20
- Maximum page size: 100
- Query parameters: page and page_size
- Invalid pages return HTTP 404

## Database indexes

### Skills
Skill names have a per-owner, case-insensitive
uniqueness constraint. This also supports related
duplicate-name checks.

### Evidence
Composite index:
(owner_id, created_at DESC, id DESC)

Purpose: support owner-filtered, newest-first
evidence queries.

### Opportunities
Composite index:
(created_at DESC, id DESC)

Purpose: support newest-first opportunity listings.

## Existing optimizations

Evidence queries use select_related("skill") to
avoid additional database queries when accessing
related skill records.

## Limitations

Indexes require storage and add write overhead.
No production performance benchmark has been conducted.

Page-number pagination also becomes less efficient
for very deep pages. Cursor pagination may be
considered if the dataset grows substantially.

## Future improvements

- Measure PostgreSQL EXPLAIN query plans
- Add representative load tests
- Review slow-query logs
- Benchmark using realistic data volumes
