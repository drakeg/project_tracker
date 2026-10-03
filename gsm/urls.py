"""URL configuration for the project tracker application."""

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("api/projects/", include("projects.api_urls")),
    path("projects/", include("projects.urls")),
    path("admin/", admin.site.urls),
]
