"""Regression tests for application readiness and liveness."""

from unittest.mock import patch

from django.db import OperationalError
from django.test import Client, SimpleTestCase
from redis.exceptions import ConnectionError as RedisConnectionError


class ReadinessTests(SimpleTestCase):
    def setUp(self):
        self.client = Client(HTTP_HOST="127.0.0.1")

    @patch("django.core.cache.cache")
    @patch("django.db.connections")
    def test_readiness_returns_200_when_dependencies_are_healthy(
        self, mock_connections, mock_cache
    ):
        mock_cache.get.return_value = "ok"

        response = self.client.get("/api/v1/health/ready/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "ok"})
        mock_connections["default"].cursor.assert_called_once()
        mock_cache.set.assert_called_once()

    @patch("django.db.connections")
    def test_readiness_returns_503_when_postgres_fails(
        self, mock_connections
    ):
        mock_connections["default"].cursor.side_effect = OperationalError(
            "private database connection details"
        )

        response = self.client.get("/api/v1/health/ready/")

        self.assertEqual(response.status_code, 503)
        self.assertEqual(
            response.json(), {"status": "unavailable"}
        )
        self.assertNotIn(
            "private database",
            response.content.decode(),
        )

    @patch("django.core.cache.cache")
    @patch("django.db.connections")
    def test_readiness_returns_503_when_redis_fails(
        self, mock_connections, mock_cache
    ):
        mock_cache.set.side_effect = RedisConnectionError(
            "private redis connection details"
        )

        response = self.client.get("/api/v1/health/ready/")

        self.assertEqual(response.status_code, 503)
        self.assertEqual(
            response.json(), {"status": "unavailable"}
        )
        self.assertNotIn(
            "private redis",
            response.content.decode(),
        )

    @patch("django.core.cache.cache")
    @patch("django.db.connections")
    def test_liveness_does_not_require_database_or_redis(
        self, mock_connections, mock_cache
    ):
        mock_connections["default"].cursor.side_effect = OperationalError(
            "database unavailable"
        )
        mock_cache.get.side_effect = RedisConnectionError(
            "redis unavailable"
        )

        response = self.client.get("/api/v1/health/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "ok"})
        mock_connections["default"].cursor.assert_not_called()
        mock_cache.get.assert_not_called()
