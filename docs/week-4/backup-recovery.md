# SkillProof API — PostgreSQL Backup and Recovery

## 1. Overview

SkillProof API uses PostgreSQL 17 with a persistent Docker volume.

The backup procedure uses PostgreSQL's custom archive format.
Backups are stored outside the Git repository and are accompanied
by SHA-256 checksums.

Scripts:
- `scripts/backup-postgres.sh`
- `scripts/verify-postgres-restore.sh`

## 2. Data protection

The primary PostgreSQL Docker volume is:

`skillproof-api_skillproof_postgres_data`

Never delete this volume as part of routine backup or restore testing.

Do not run `docker compose down -v` against the live deployment.

## 3. Create a backup

From the repository root:

```bash
./scripts/backup-postgres.sh
```

Default destination:

`$HOME/skillproof-backups/`

The backup script:

1. Verifies that PostgreSQL accepts connections.
2. Creates a custom-format database archive.
3. Checks that the archive is nonempty.
4. Validates the archive table of contents.
5. Saves the archive with owner-only permissions.
6. Generates a SHA-256 checksum.

Example files:

- `skillproof-YYYYMMDD-HHMMSS.dump`
- `skillproof-YYYYMMDD-HHMMSS.dump.sha256`

## 4. Verify backup integrity

```bash
shasum -a 256 -c \
  "$HOME/skillproof-backups/skillproof-YYYYMMDD-HHMMSS.dump.sha256"
```

The expected result ends with `OK`.

The checksum detects changes to the backup file.
It does not replace a full restore verification.

## 5. Perform an isolated restore test

```bash
./scripts/verify-postgres-restore.sh
```

To test a specific backup:

```bash
./scripts/verify-postgres-restore.sh \
  "$HOME/skillproof-backups/skillproof-YYYYMMDD-HHMMSS.dump"
```

The script:

1. Checks the backup checksum.
2. Checks the original PostgreSQL service.
3. Starts a temporary, network-isolated PostgreSQL 17 container.
4. Restores the archive using `pg_restore`.
5. Compares public table names and row counts.
6. Removes the temporary container.

The restore test does not drop or replace the original database.

## 6. Verification limitations

The restore test compares the backup with the current live
database. If records change after the backup was created, row
counts may legitimately differ.

Matching table names and row counts do not prove that every
individual record is identical.

Archive inspection alone does not guarantee full recoverability.
A successful isolated restore is required for stronger assurance.

## 7. Recovery objectives

Recovery Point Objective (RPO):
Not yet formally established.

Recovery Time Objective (RTO):
Not yet formally established.

These objectives must be defined based on business requirements
and measured through repeated recovery exercises.

No production recovery-time guarantee has been established.

## 8. Suggested backup policy

For a future production deployment:

- Schedule backups at least daily, subject to the agreed RPO.
- Maintain a documented retention policy.
- Keep multiple recovery points.
- Encrypt backups before transferring them off-machine.
- Store backup copies in a separate location or cloud account.
- Restrict access to authorized administrators.
- Test restoration periodically.
- Monitor failed backups and missing backup files.

The current scripts create local backups only. They do not
automatically schedule backups, encrypt files or upload
copies to remote storage.

## 9. Full production recovery

The provided restore-verification script is for testing only.

A full production recovery requires a separately approved
runbook covering:

- Incident assessment
- Selection and verification of a recovery point
- Safe handling of current database data
- Recovery into a new PostgreSQL instance
- Schema and application compatibility checks
- Application smoke tests
- Cutover and rollback procedures

Never overwrite the production database using the isolated
restore-verification script.

## 10. Week 4 local validation

On November 7, 2026:

- A PostgreSQL custom-format backup was created.
- Its SHA-256 checksum passed validation.
- The archive restored successfully into PostgreSQL 17.
- All 13 public tables were found in the restored database.
- Source and restored table row counts matched.
- The temporary restore container was removed.
- The original PostgreSQL service remained healthy.
- The SkillProof API returned HTTP 200.

This validation demonstrates successful local recovery testing,
not a production disaster-recovery certification.
