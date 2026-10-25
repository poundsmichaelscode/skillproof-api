"""Consistent public-facing responses for handled DRF API exceptions."""
from rest_framework.views import exception_handler as drf_exception_handler


CODES = {
    400: "VALIDATION_ERROR",
    401: "AUTHENTICATION_FAILED",
    403: "PERMISSION_DENIED",
    404: "NOT_FOUND",
    405: "METHOD_NOT_ALLOWED",
    406: "NOT_ACCEPTABLE",
    415: "UNSUPPORTED_MEDIA_TYPE",
    429: "RATE_LIMITED",
}

MESSAGES = {
    400: "Invalid request data.",
    401: "Authentication credentials were not provided or are invalid.",
    403: "You do not have permission to perform this action.",
    404: "The requested resource was not found.",
    405: "This HTTP method is not allowed.",
    429: "Too many requests.",
}


def api_exception_handler(exc, context):
    response = drf_exception_handler(exc, context)
    if response is None:
        # Do not disguise unexpected bugs as validation errors.
        # Django handles unexpected errors and hides tracebacks when DEBUG=False.
        return None

    status = response.status_code
    original = response.data
    data = {
        "code": CODES.get(status, "API_ERROR"),
        "message": MESSAGES.get(status, "The request could not be completed."),
    }
    # Keep validation messages for clients. Do not expose arbitrary exception
    # descriptions for auth, permission, and lookup failures.
    if status == 400:
        data["details"] = original

    response.data = {"error": data}
    return response
