from types import SimpleNamespace

from django.conf import settings
from django.core.cache import cache
from django.test import SimpleTestCase
from rest_framework.request import Request
from rest_framework.test import APIRequestFactory
from rest_framework.throttling import ScopedRateThrottle


class RedisThrottleTests(SimpleTestCase):
    def test_login_throttle_shares_request_history(self):
        self.assertEqual(
            settings.CACHES["default"]["BACKEND"],
            "django.core.cache.backends.redis.RedisCache",
        )

        factory = APIRequestFactory()
        view = SimpleNamespace(throttle_scope="auth_login")

        def make_request():
            return Request(
                factory.post(
                    "/api/v1/auth/token/",
                    REMOTE_ADDR="192.0.2.231",
                )
            )

        initial_throttle = ScopedRateThrottle()
        initial_throttle.scope = view.throttle_scope
        cache_key = initial_throttle.get_cache_key(
            make_request(),
            view,
        )

        self.assertIsNotNone(cache_key)
        cache.delete(cache_key)

        try:
            # Different instances must share the request counter.
            for _ in range(10):
                throttle = ScopedRateThrottle()
                self.assertTrue(
                    throttle.allow_request(make_request(), view)
                )

            # The 11th request must exceed the login limit.
            throttle = ScopedRateThrottle()
            self.assertFalse(
                throttle.allow_request(make_request(), view)
            )

            self.assertEqual(len(cache.get(cache_key)), 10)
        finally:
            cache.delete(cache_key)
