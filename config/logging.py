"""Structured application logging without request secrets."""

import json
import logging
from datetime import datetime, timezone


class JSONFormatter(logging.Formatter):
    """Format allowlisted log fields as JSON."""

    def format(self, record):
        payload = {
            "timestamp": datetime.now(timezone.utc)
            .isoformat(timespec="milliseconds")
            .replace("+00:00", "Z"),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }

        for field in (
            "request_id",
            "method",
            "status_code",
            "duration_ms",
        ):
            value = getattr(record, field, None)
            if value is not None:
                payload[field] = value

        return json.dumps(payload)
