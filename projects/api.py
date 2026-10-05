"""API viewsets for project tracker resources."""

from rest_framework import viewsets

from .models import Contact, Keyword, Status, Tracker
from .serializers import (
    ContactSerializer,
    FullTrackerSerializer,
    KeywordSerializer,
    StatusSerializer,
)


class TrackerViewSet(viewsets.ModelViewSet):
    """CRUD API for project trackers."""

    serializer_class = FullTrackerSerializer
    queryset = Tracker.objects.all()


class ContactViewSet(viewsets.ModelViewSet):
    """CRUD API for contacts."""

    serializer_class = ContactSerializer
    queryset = Contact.objects.all()


class KeywordViewSet(viewsets.ModelViewSet):
    """CRUD API for keywords."""

    serializer_class = KeywordSerializer
    queryset = Keyword.objects.all()


class StatusViewSet(viewsets.ModelViewSet):
    """CRUD API for status values."""

    serializer_class = StatusSerializer
    queryset = Status.objects.all()
