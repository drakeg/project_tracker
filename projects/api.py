"""API viewsets for project tracker resources."""

from rest_framework import viewsets

from .models import (
    Alignment,
    Comment,
    Contact,
    DTContact,
    Keyword,
    MaturityModel,
    Status,
    Task,
    Tracker,
    Update,
)
from .serializers import (
    AlignmentSerializer,
    CommentSerializer,
    ContactSerializer,
    DTContactSerializer,
    FullTrackerSerializer,
    KeywordSerializer,
    MaturityModelSerializer,
    StatusSerializer,
    TaskSerializer,
    UpdateSerializer,
)


class TrackerViewSet(viewsets.ModelViewSet):
    """CRUD API for project trackers."""

    serializer_class = FullTrackerSerializer
    queryset = Tracker.objects.all()


class ContactViewSet(viewsets.ModelViewSet):
    """CRUD API for contacts."""

    serializer_class = ContactSerializer
    queryset = Contact.objects.all()


class DTContactViewSet(viewsets.ModelViewSet):
    """CRUD API for delivery-team contacts."""

    serializer_class = DTContactSerializer
    queryset = DTContact.objects.all()


class TaskViewSet(viewsets.ModelViewSet):
    """CRUD API for task values."""

    serializer_class = TaskSerializer
    queryset = Task.objects.all()


class AlignmentViewSet(viewsets.ModelViewSet):
    """CRUD API for alignment values."""

    serializer_class = AlignmentSerializer
    queryset = Alignment.objects.all()


class MaturityModelViewSet(viewsets.ModelViewSet):
    """CRUD API for maturity-model values."""

    serializer_class = MaturityModelSerializer
    queryset = MaturityModel.objects.all()


class CommentViewSet(viewsets.ModelViewSet):
    """CRUD API for tracker comments."""

    serializer_class = CommentSerializer
    queryset = Comment.objects.all()


class UpdateViewSet(viewsets.ModelViewSet):
    """CRUD API for tracker updates."""

    serializer_class = UpdateSerializer
    queryset = Update.objects.all()


class KeywordViewSet(viewsets.ModelViewSet):
    """CRUD API for keywords."""

    serializer_class = KeywordSerializer
    queryset = Keyword.objects.all()


class StatusViewSet(viewsets.ModelViewSet):
    """CRUD API for status values."""

    serializer_class = StatusSerializer
    queryset = Status.objects.all()
