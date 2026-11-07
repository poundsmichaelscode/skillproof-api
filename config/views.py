from drf_spectacular.utils import extend_schema, inline_serializer
from rest_framework import serializers
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response


@extend_schema(
    responses={
        200: inline_serializer(
            name="HealthResponse",
            fields={"status": serializers.CharField()},
        )
    },
    description="Public application health check.",
)
@api_view(["GET"])
@permission_classes([AllowAny])
def health_check(request):
    """Return the application liveness status."""
    return Response({"status": "ok"})


@extend_schema(
    responses={
        200: inline_serializer(
            name="ReadinessResponse",
            fields={"status": serializers.CharField()},
        ),
        503: inline_serializer(
            name="ReadinessUnavailableResponse",
            fields={"status": serializers.CharField()},
        ),
    },
    description="Check required PostgreSQL and Redis dependencies.",
)
@api_view(["GET"])
@permission_classes([AllowAny])
def readiness_check(request):
    """Return readiness without exposing dependency credentials."""
    from django.core.cache import cache
    from django.db import connections

    try:
        with connections["default"].cursor() as cursor:
            cursor.execute("SELECT 1")
            cursor.fetchone()

        cache.set("health:readiness", "ok", timeout=10)

        if cache.get("health:readiness") != "ok":
            return Response(
                {"status": "unavailable"},
                status=503,
            )
    except Exception:
        return Response(
            {"status": "unavailable"},
            status=503,
        )

    return Response({"status": "ok"})
