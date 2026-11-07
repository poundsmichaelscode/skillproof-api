"""Authentication throttling with explicit Redis outage handling."""

import logging

from redis.exceptions import RedisError
from rest_framework.exceptions import APIException
from rest_framework.throttling import ScopedRateThrottle

logger = logging.getLogger("skillproof.security")


class AuthenticationThrottleUnavailable(APIException):
    status_code = 503
    default_detail = (
        "Authentication is temporarily unavailable. "
        "Please try again later."
    )
    default_code = "authentication_throttle_unavailable"


class SafeScopedRateThrottle(ScopedRateThrottle):
    """Fail closed when the shared throttle cache is unavailable."""

    def allow_request(self, request, view):
        try:
            return super().allow_request(request, view)
        except (RedisError, OSError):
            logger.warning("authentication_throttle_cache_unavailable")
            raise AuthenticationThrottleUnavailable()
