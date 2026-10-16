"""URL configuration for SkillProof API."""

from django.contrib import admin
from django.urls import path

from config.views import health_check

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "api/v1/health/",
        health_check,
        name="health-check",
    ),
]
