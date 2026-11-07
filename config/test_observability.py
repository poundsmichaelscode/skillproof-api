import json
import logging
from uuid import UUID

from django.test import SimpleTestCase

from config.logging import JSONFormatter


class RequestObservabilityTests(SimpleTestCase):
    def test_health_response_has_request_id(self):
        response = self.client.get("/api/v1/health/")

        self.assertEqual(response.status_code, 200)

        request_id = response["X-Request-ID"]
        self.assertEqual(str(UUID(request_id)), request_id)

    def test_each_request_gets_unique_id(self):
        first = self.client.get("/api/v1/health/")
        second = self.client.get("/api/v1/health/")

        self.assertNotEqual(
            first["X-Request-ID"],
            second["X-Request-ID"],
        )

    def test_request_log_is_structured_and_safe(self):
        with self.assertLogs(
            "skillproof.requests",
            level="INFO",
        ) as captured:
            response = self.client.get(
                "/api/v1/health/?token=secret-in-query",
                HTTP_AUTHORIZATION="Bearer secret-token",
            )

        record = captured.records[-1]
        payload = json.loads(JSONFormatter().format(record))

        self.assertEqual(payload["message"], "request_completed")
        self.assertEqual(payload["method"], "GET")
        self.assertEqual(response.status_code, 401)
        self.assertEqual(payload["status_code"], response.status_code)
        self.assertEqual(
            payload["request_id"],
            response["X-Request-ID"],
        )
        self.assertGreaterEqual(payload["duration_ms"], 0)

        serialized = json.dumps(payload)
        self.assertNotIn("secret-token", serialized)
        self.assertNotIn("secret-in-query", serialized)
        self.assertNotIn("Authorization", serialized)

    def test_formatter_produces_valid_json(self):
        record = logging.LogRecord(
            name="skillproof.requests",
            level=logging.INFO,
            pathname=__file__,
            lineno=1,
            msg="request_completed",
            args=(),
            exc_info=None,
        )

        payload = json.loads(JSONFormatter().format(record))

        self.assertEqual(payload["level"], "INFO")
        self.assertIn("timestamp", payload)
        self.assertEqual(
            payload["message"],
            "request_completed",
        )
