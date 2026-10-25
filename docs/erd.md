# SkillProof API — Week 2 Entity Relationship Diagram

The following Mermaid diagram depicts the **implemented** Django data models. It renders directly in GitHub Markdown and can be used in a mentor presentation.

```mermaid
erDiagram
    USER ||--o{ SKILL : owns
    USER ||--o{ EVIDENCE : owns
    USER ||--o{ OPPORTUNITY : publishes
    SKILL ||--o{ EVIDENCE : proves

    USER {
        bigint id PK
        string username UK
        string email "validated in application"
        string password "hashed"
        string first_name
        string last_name
        datetime date_joined
    }
    SKILL {
        bigint id PK
        bigint owner_id FK
        string name "max 150; unique per owner ignoring case"
        string proficiency "beginner | intermediate | advanced"
        text description
        datetime created_at
        datetime updated_at
    }
    EVIDENCE {
        bigint id PK
        bigint owner_id FK
        bigint skill_id FK
        string title "max 200"
        text description
        string evidence_url
        datetime created_at
        datetime updated_at
    }
    OPPORTUNITY {
        bigint id PK
        bigint owner_id FK
        string title "max 200"
        string organization "max 200"
        text description
        string application_url
        date closing_date "optional"
        datetime created_at
        datetime updated_at
    }
```

## Relations and safeguards

| Relationship | Cardinality | Delete behavior | API rule |
| --- | --- | --- | --- |
| User → Skill | One-to-many | CASCADE | Owner-only list and detail operations |
| User → Evidence | One-to-many | CASCADE | Owner-only CRUD; client cannot override owner |
| Skill → Evidence | One-to-many | CASCADE | Evidence may reference only the owner's Skill |
| User → Opportunity | One-to-many | CASCADE | Authenticated read; owner/staff edit and delete |

**Important implementation details:** Email uniqueness is checked at the serializer level, not yet with a database unique constraint. Evidence `owner_id = skill.owner_id` is checked in model/serializer paths, not enforced as a cross-table database constraint. Both are recorded in the security review.

See [architecture.md](architecture.md) for the API flow and [week-2-security-review.md](week-2-security-review.md) for the six known risks.
