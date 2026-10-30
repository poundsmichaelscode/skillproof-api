from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)

"""URL configuration for SkillProof API."""

from django.contrib import admin
from django.urls import include, path

from config.views import health_check

urlpatterns = [

    path(
        "api/schema/",
        SpectacularAPIView.as_view(),
        name="schema",
    ),
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "api/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
    path("api/v1/opportunities/", include("apps.opportunities.urls")),
    path("api/v1/evidence/", include("apps.evidence.urls")),
    path("api/v1/auth/", include("apps.accounts.urls")),
    path("api/v1/skills/", include("apps.skills.urls")),
    path("admin/", admin.site.urls),
    path(
        "api/v1/health/",
        health_check,
        name="health-check",
    ),
]
