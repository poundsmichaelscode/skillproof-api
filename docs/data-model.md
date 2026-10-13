# SkillProof API — Data Model

## Overview

SkillProof uses PostgreSQL with the Django ORM.

The MVP contains four primary entities:

1. User
2. Skill
3. Evidence
4. Opportunity

## 1. User

Uses Django's built-in authentication model.

Important fields:
- id: primary key
- username: unique username
- email: email address
- password: securely hashed password
- first_name: optional
- last_name: optional
- date_joined: account creation timestamp

A user can own multiple skills, evidence records,
and opportunities.

## 2. Skill

Fields:
- id: primary key
- owner: ForeignKey(User)
- name: CharField(max_length=150)
- description: TextField(blank=True)
- proficiency: CharField with beginner,
  intermediate, and advanced choices
- created_at: DateTimeField(auto_now_add=True)
- updated_at: DateTimeField(auto_now=True)

Relationships:
- One user can own many skills.
- One skill can have many evidence records.

Constraints:
- A user cannot create duplicate skills with
  the same normalized name.
- Name cannot be empty.
- Owner is assigned from the authenticated user.

Deletion:
- Deleting a user deletes their skills.
- Deleting a skill deletes its related evidence.

## 3. Evidence

Fields:
- id: primary key
- owner: ForeignKey(User)
- skill: ForeignKey(Skill)
- title: CharField(max_length=200)
- description: TextField(blank=True)
- evidence_url: URLField()
- created_at: DateTimeField(auto_now_add=True)
- updated_at: DateTimeField(auto_now=True)

Relationships:
- One user can own many evidence records.
- Each evidence record belongs to one skill.
- Each evidence record belongs to one user.

Constraints:
- The evidence owner must match the skill owner.
- Evidence URLs must be valid.
- Title cannot be empty.
- Users cannot access another user's private
  evidence records.

Deletion:
- Deleting the parent skill deletes its evidence.
- Deleting a user deletes their evidence.

## 4. Opportunity

Fields:
- id: primary key
- owner: ForeignKey(User)
- title: CharField(max_length=200)
- organization: CharField(max_length=200)
- description: TextField(blank=True)
- application_url: URLField()
- closing_date: DateField(null=True, blank=True)
- created_at: DateTimeField(auto_now_add=True)
- updated_at: DateTimeField(auto_now=True)

Relationships:
- One user can create multiple opportunities.
- Each opportunity has one owner.

Permissions:
- Authenticated users can browse opportunities.
- Only the owner or an authorized administrator
  can modify or delete an opportunity.

Deletion:
- Deleting the owner deletes their opportunities.

## Ownership and Security

- All create operations assign the owner server-side.
- Clients cannot override the owner field.
- Private querysets are filtered by request.user.
- Evidence creation validates skill ownership.
- Update and delete operations enforce ownership.
- Anonymous requests cannot access private records.

## Relationship Summary

User (1) -> (N) Skill
User (1) -> (N) Evidence
User (1) -> (N) Opportunity
Skill (1) -> (N) Evidence

## Design Decisions

- Use Django's built-in User model.
- Use integer primary keys for simplicity.
- Use PostgreSQL foreign keys for referential integrity.
- Use cascading deletion for dependent records.
- Store evidence as URLs, not uploaded files.
- Defer advanced search and recommendation features.
- Use Django ORM migrations for schema changes.

## Implementation Notes

- Enforce ownership in DRF permissions and querysets.
- Validate evidence and skill relationships in serializers.
- Enforce normalized skill-name uniqueness using an
  appropriate database constraint during implementation.
- Review query patterns before introducing indexes.
- Add tests covering cross-user access and deletion.
