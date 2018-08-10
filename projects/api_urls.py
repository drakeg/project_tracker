"""
This module contains URLPatterns specific to the API.  This is not named
according to any specific naming-convention (and actually probably should be named something else),
but seemed reasonably consistent with the api.py module name
"""
from rest_framework import routers

from . import api

API_ROUTER = routers.SimpleRouter()
API_ROUTER.register(r'trackers', api.TrackerViewSet)
API_ROUTER.register(r'contacts', api.ContactViewSet)

urlpatterns = API_ROUTER.urls
