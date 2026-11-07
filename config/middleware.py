"""Request correlation and safe HTTP access logging."""

import logging
import time
from uuid import uuid4


logger = logging.getLogger("skillproof.requests")


class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request_id = str(uuid4())
        request.request_id = request_id

        start = time.perf_counter()
        status_code = 500

        try:
            response = self.get_response(request)
            status_code = response.status_code
            response["X-Request-ID"] = request_id
            return response
        finally:
            duration_ms = round(
                (time.perf_counter() - start) * 1000,
                2,
            )

            logger.info(
                "request_completed",
                extra={
                    "request_id": request_id,
                    "method": request.method,
                    "status_code": status_code,
                    "duration_ms": duration_ms,
                },
            )
