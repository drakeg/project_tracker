"""API viewsets for project tracker resources."""

from rest_framework import filters, viewsets

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
    queryset = Tracker.objects.select_related(
        "task",
        "contact",
        "dtcontact",
        "status",
        "alignment",
        "maturitymodel",
    ).prefetch_related("keywords")
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["title"]
    ordering_fields = ["title", "start_date", "end_date", "create_date"]
    ordering = ["title"]

    def get_queryset(self):
        queryset = super().get_queryset()
        query_params = self.request.query_params

        relationship_filters = {
            "status": "status_id",
            "task": "task_id",
            "contact": "contact_id",
            "dtcontact": "dtcontact_id",
            "alignment": "alignment_id",
            "maturitymodel": "maturitymodel_id",
            "keyword": "keywords__id",
        }
        for parameter, field in relationship_filters.items():
            value = query_params.get(parameter)
            if value:
                queryset = queryset.filter(**{field: value})

        start_date_gte = query_params.get("start_date_gte")
        if start_date_gte:
            queryset = queryset.filter(start_date__gte=start_date_gte)

        end_date_lte = query_params.get("end_date_lte")
        if end_date_lte:
            queryset = queryset.filter(end_date__lte=end_date_lte)

        return queryset.distinct()


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
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["comment_text"]
    ordering_fields = ["comment_date"]
    ordering = ["-comment_date"]

    def get_queryset(self):
        queryset = super().get_queryset()
        query_params = self.request.query_params

        tracker = query_params.get("tracker")
        if tracker:
            queryset = queryset.filter(comment_tracker_id=tracker)

        user = query_params.get("user")
        if user:
            queryset = queryset.filter(comment_user_id=user)

        date_gte = query_params.get("date_gte")
        if date_gte:
            queryset = queryset.filter(comment_date__gte=date_gte)

        date_lte = query_params.get("date_lte")
        if date_lte:
            queryset = queryset.filter(comment_date__lte=date_lte)

        return queryset


class UpdateViewSet(viewsets.ModelViewSet):
    """CRUD API for tracker updates."""

    serializer_class = UpdateSerializer
    queryset = Update.objects.all()
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["update_text"]
    ordering_fields = ["update_date"]
    ordering = ["-update_date"]

    def get_queryset(self):
        queryset = super().get_queryset()
        query_params = self.request.query_params

        tracker = query_params.get("tracker")
        if tracker:
            queryset = queryset.filter(update_tracker_id=tracker)

        user = query_params.get("user")
        if user:
            queryset = queryset.filter(update_user_id=user)

        date_gte = query_params.get("date_gte")
        if date_gte:
            queryset = queryset.filter(update_date__gte=date_gte)

        date_lte = query_params.get("date_lte")
        if date_lte:
            queryset = queryset.filter(update_date__lte=date_lte)

        return queryset


class KeywordViewSet(viewsets.ModelViewSet):
    """CRUD API for keywords."""

    serializer_class = KeywordSerializer
    queryset = Keyword.objects.all()


class StatusViewSet(viewsets.ModelViewSet):
    """CRUD API for status values."""

    serializer_class = StatusSerializer
    queryset = Status.objects.all()
