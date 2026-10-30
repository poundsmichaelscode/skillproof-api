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
