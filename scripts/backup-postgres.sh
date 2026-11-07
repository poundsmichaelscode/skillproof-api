#!/usr/bin/env bash
set -Eeuo pipefail

cd "$(dirname "$0")/.."

ENV_FILE="${ENV_FILE:-.env}"
BACKUP_DIR="${BACKUP_DIR:-$HOME/skillproof-backups}"

if [[ ! -f "$ENV_FILE" ]]; then
  echo "FAIL: Compose environment file not found"
  exit 1
fi

umask 077
mkdir -p "$BACKUP_DIR"
chmod 700 "$BACKUP_DIR"

STAMP="$(date -u +%Y%m%d-%H%M%S)"
BACKUP_FILE="$BACKUP_DIR/skillproof-$STAMP.dump"

# Never overwrite an existing archive.
if [[ -e "$BACKUP_FILE" ]]; then
  echo "FAIL: Backup filename already exists"
  exit 1
fi

TMP_FILE="$(mktemp "$BACKUP_DIR/.skillproof-XXXXXXXX.dump")"

cleanup() {
  rm -f "$TMP_FILE"
}
trap cleanup EXIT

echo "===== CHECK DATABASE ====="

docker compose --env-file "$ENV_FILE" exec -T db \
  sh -c 'pg_isready -U "$POSTGRES_USER" -d "$POSTGRES_DB"'

echo "===== CREATE BACKUP ====="

docker compose --env-file "$ENV_FILE" exec -T db \
  sh -c 'exec pg_dump -U "$POSTGRES_USER" -d "$POSTGRES_DB" --format=custom --no-owner --no-acl' \
  > "$TMP_FILE"

if [[ ! -s "$TMP_FILE" ]]; then
  echo "FAIL: Backup is empty"
  exit 1
fi

echo "===== VALIDATE ARCHIVE ====="

docker compose --env-file "$ENV_FILE" exec -T db \
  pg_restore --list < "$TMP_FILE" > /dev/null

mv "$TMP_FILE" "$BACKUP_FILE"
chmod 600 "$BACKUP_FILE"

echo "===== GENERATE CHECKSUM ====="

shasum -a 256 "$BACKUP_FILE" > "$BACKUP_FILE.sha256"
chmod 600 "$BACKUP_FILE.sha256"

echo "===== BACKUP COMPLETE ====="
ls -lh "$BACKUP_FILE"
echo "Backup: $BACKUP_FILE"
echo "Checksum: $BACKUP_FILE.sha256"
echo "PASS: PostgreSQL backup created and archive inspected"
