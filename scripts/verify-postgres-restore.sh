#!/usr/bin/env bash
set -Eeuo pipefail

cd "$(dirname "$0")/.."

BACKUP_DIR="${BACKUP_DIR:-$HOME/skillproof-backups}"
ENV_FILE="${ENV_FILE:-.env}"
CONTAINER="skillproof-restore-test"

BACKUP_FILE="${1:-$(find "$BACKUP_DIR" -maxdepth 1 -type f -name 'skillproof-*.dump' | sort | tail -1)}"

if [[ -z "$BACKUP_FILE" || ! -f "$BACKUP_FILE" ]]; then
  echo "FAIL: Backup file not found"
  exit 1
fi

if [[ ! -f "$BACKUP_FILE.sha256" ]]; then
  echo "FAIL: Backup checksum missing"
  exit 1
fi

if [[ ! -f "$ENV_FILE" ]]; then
  echo "FAIL: Compose environment file missing"
  exit 1
fi

if docker ps -a --format '{{.Names}}' | grep -Fxq "$CONTAINER"; then
  echo "FAIL: Restore test container already exists"
  exit 1
fi

SOURCE_ROWS="$(mktemp)"
RESTORED_ROWS="$(mktemp)"
STARTED=0

cleanup() {
  if [[ "$STARTED" -eq 1 ]]; then
    docker stop "$CONTAINER" >/dev/null 2>&1 || true
  fi
  rm -f "$SOURCE_ROWS" "$RESTORED_ROWS"
}
trap cleanup EXIT

echo "===== VERIFY BACKUP CHECKSUM ====="
shasum -a 256 -c "$BACKUP_FILE.sha256"

echo "===== CHECK ORIGINAL DATABASE ====="
docker compose --env-file "$ENV_FILE" exec -T db \
  sh -c 'pg_isready -U "$POSTGRES_USER" -d "$POSTGRES_DB"'

echo "===== START ISOLATED POSTGRESQL ====="
docker run -d --rm \
  --name "$CONTAINER" \
  --network none \
  --tmpfs /var/lib/postgresql/data:rw,size=1g \
  -e POSTGRES_HOST_AUTH_METHOD=trust \
  -e POSTGRES_USER=restore_test \
  -e POSTGRES_DB=restore_test \
  postgres:17 >/dev/null

STARTED=1

echo "===== WAIT FOR RESTORE DATABASE ====="
READY=0

for attempt in $(seq 1 30); do
  if docker exec "$CONTAINER" \
    pg_isready -U restore_test -d restore_test \
    >/dev/null 2>&1; then
    READY=1
    break
  fi
  sleep 1
done

if [[ "$READY" -ne 1 ]]; then
  echo "FAIL: Restore database did not become ready"
  exit 1
fi

echo "===== RESTORE BACKUP ====="
docker exec -i "$CONTAINER" \
  pg_restore \
    -U restore_test \
    -d restore_test \
    --no-owner \
    --no-acl \
    --exit-on-error \
    < "$BACKUP_FILE"

echo "===== COUNT SOURCE TABLE ROWS ====="

docker compose --env-file "$ENV_FILE" exec -T db \
  sh -c 'psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -At -F "|"' \
  <<'SQL' | LC_ALL=C sort > "$SOURCE_ROWS"
SELECT format(
  'SELECT %L, count(*) FROM %I.%I',
  tablename, schemaname, tablename
)
FROM pg_catalog.pg_tables
WHERE schemaname = 'public'
ORDER BY tablename
\gexec
SQL

echo "===== COUNT RESTORED TABLE ROWS ====="

docker exec -i "$CONTAINER" \
  psql -U restore_test -d restore_test -At -F "|" \
  <<'SQL' | LC_ALL=C sort > "$RESTORED_ROWS"
SELECT format(
  'SELECT %L, count(*) FROM %I.%I',
  tablename, schemaname, tablename
)
FROM pg_catalog.pg_tables
WHERE schemaname = 'public'
ORDER BY tablename
\gexec
SQL

echo "===== COMPARE TABLES AND ROW COUNTS ====="

if ! diff -u "$SOURCE_ROWS" "$RESTORED_ROWS"; then
  echo "FAIL: Source and restored row counts differ"
  echo "Note: Changes to the live database after backup can cause differences."
  exit 1
fi

TABLE_COUNT="$(wc -l < "$RESTORED_ROWS" | tr -d ' ')"

if [[ "$TABLE_COUNT" -eq 0 ]]; then
  echo "FAIL: No restored public tables found"
  exit 1
fi

echo "PASS: Matching table names and row counts"
echo "Verified public tables: $TABLE_COUNT"

echo "===== RESTORE VERIFICATION COMPLETE ====="
echo "PASS: Backup checksum verified"
echo "PASS: Isolated restore completed"
echo "PASS: Table and row counts matched"
echo "PASS: Original database not modified by restore"
