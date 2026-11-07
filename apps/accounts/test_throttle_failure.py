"""Verify that authentication throttles fail closed."""

from types import SimpleNamespace
from unittest.mock import patch

from django.test import SimpleTestCase
from redis.exceptions import ConnectionError as RedisConnectionError
from rest_framework.request import Request
from rest_framework.test import APIRequestFactory, APIClient
from rest_framework.throttling import ScopedRateThrottle

from apps.accounts.throttles import (
    AuthenticationThrottleUnavailable,
    SafeScopedRateThrottle,
)


class ThrottleFailureTests(SimpleTestCase):
    def setUp(self):
        self.factory = APIRequestFactory()

    def test_redis_failure_does_not_allow_request(self):
        request = Request(
            self.factory.post(
                "/api/v1/auth/token/",
                REMOTE_ADDR="192.0.2.10",
            )
        )
        view = SimpleNamespace(throttle_scope="auth_login")

        with patch.object(
            ScopedRateThrottle,
            "allow_request",
            side_effect=RedisConnectionError("test outage"),
        ):
            with self.assertRaises(
                AuthenticationThrottleUnavailable
            ) as context:
                SafeScopedRateThrottle().allow_request(
                    request, view
                )

        self.assertEqual(
            context.exception.status_code, 503
        )

    def test_login_returns_503_when_redis_fails(self):
        client = APIClient()

        with patch.object(
            ScopedRateThrottle,
            "allow_request",
            side_effect=RedisConnectionError("test outage"),
        ):
            response = client.post(
                "/api/v1/auth/token/",
                {"username": "test", "password": "test"},
                format="json",
            )

        self.assertEqual(response.status_code, 503)
        self.assertNotIn(
            "test outage",
            response.content.decode(),
        )

    def test_registration_returns_503_when_redis_fails(self):
        client = APIClient()

        with patch.object(
            ScopedRateThrottle,
            "allow_request",
            side_effect=RedisConnectionError("test outage"),
        ):
            response = client.post(
                "/api/v1/auth/register/",
                {},
                format="json",
            )

        self.assertEqual(response.status_code, 503)
        self.assertNotIn("test outage", response.content.decode())

    def test_token_refresh_returns_503_when_redis_fails(self):
        client = APIClient()

        with patch.object(
            ScopedRateThrottle,
            "allow_request",
            side_effect=RedisConnectionError("test outage"),
        ):
            response = client.post(
                "/api/v1/auth/token/refresh/",
                {"refresh": "invalid"},
                format="json",
            )

        self.assertEqual(response.status_code, 503)
        self.assertNotIn("test outage", response.content.decode())
