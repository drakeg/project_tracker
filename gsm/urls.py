"""URL configuration for the project tracker application."""

from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView
from rest_framework.permissions import AllowAny
from rest_framework.schemas import get_schema_view

schema_view = get_schema_view(
    title="Project Tracker API",
    description="OpenAPI schema for the project tracker REST API.",
    version="1.0.0",
    permission_classes=[AllowAny],
    patterns=[
        path("api/projects/", include("projects.api_urls")),
    ],
)

urlpatterns = [
    path("api/projects/", include("projects.api_urls")),
    path("api-auth/", include("rest_framework.urls")),
    path("api/schema/", schema_view, name="openapi-schema"),
    path(
        "api/docs/",
        TemplateView.as_view(
            template_name="swagger-ui.html",
            extra_context={"schema_url": "openapi-schema"},
        ),
        name="swagger-ui",
    ),
    path("projects/", include("projects.urls")),
    path("admin/", admin.site.urls),
]
