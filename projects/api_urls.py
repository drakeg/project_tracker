"""API URL routes."""

from rest_framework import routers

from . import api

API_ROUTER = routers.SimpleRouter()
API_ROUTER.register(r"trackers", api.TrackerViewSet)
API_ROUTER.register(r"contacts", api.ContactViewSet)
API_ROUTER.register(r"keywords", api.KeywordViewSet)
API_ROUTER.register(r"status", api.StatusViewSet)

urlpatterns = API_ROUTER.urls
