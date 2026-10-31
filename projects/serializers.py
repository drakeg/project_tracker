"""Serializers for the project tracker API."""

from rest_framework import serializers

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


class TaskSerializer(serializers.ModelSerializer):
    """Serializer for task values."""

    class Meta:
        model = Task
        fields = "__all__"


class DTContactSerializer(serializers.ModelSerializer):
    """Serializer for delivery-team contacts."""

    class Meta:
        model = DTContact
        fields = "__all__"


class AlignmentSerializer(serializers.ModelSerializer):
    """Serializer for alignment values."""

    class Meta:
        model = Alignment
        fields = "__all__"


class MaturityModelSerializer(serializers.ModelSerializer):
    """Serializer for maturity-model values."""

    class Meta:
        model = MaturityModel
        fields = "__all__"


class CommentSerializer(serializers.ModelSerializer):
    """Serializer for tracker comments."""

    class Meta:
        model = Comment
        fields = "__all__"


class UpdateSerializer(serializers.ModelSerializer):
    """Serializer for tracker updates."""

    class Meta:
        model = Update
        fields = "__all__"


class StatusSerializer(serializers.ModelSerializer):
    """Serializer for project status values."""

    def validate_status_text(self, value):
        query = Status.objects.filter(status_text__iexact=value)
        if self.instance is not None:
            query = query.exclude(pk=self.instance.pk)
        if query.exists():
            raise serializers.ValidationError("Status already exists.")
        return value

    class Meta:
        model = Status
        fields = ["status_text"]


class KeywordSerializer(serializers.ModelSerializer):
    """Serializer for project keywords."""

    def validate_keyword_text(self, value):
        query = Keyword.objects.filter(keyword_text__iexact=value)
        if self.instance is not None:
            query = query.exclude(pk=self.instance.pk)
        if query.exists():
            raise serializers.ValidationError("Keyword already exists.")
        return value

    class Meta:
        model = Keyword
        fields = ["keyword_text"]


class SimpleTrackerSerializer(serializers.ModelSerializer):
    """Compact tracker representation used by contact responses."""

    status = StatusSerializer()

    class Meta:
        model = Tracker
        fields = [
            "title",
            "status",
            "create_date",
            "start_date",
            "end_date",
        ]


class ContactSerializer(serializers.ModelSerializer):
    """Serializer for contacts and their trackers."""

    trackers = SimpleTrackerSerializer(
        source="tracker_set",
        many=True,
        read_only=True,
    )

    class Meta:
        model = Contact
        fields = "__all__"


class RelatedContactSerializer(serializers.ModelSerializer):
    """Nested contact representation used by tracker writes."""

    class Meta:
        model = Contact
        fields = [
            "contact_fname",
            "contact_lname",
            "contact_phone",
        ]


class FullTrackerSerializer(serializers.ModelSerializer):
    """Full tracker representation with writable relationship inputs."""

    contact = RelatedContactSerializer(required=False, allow_null=True)
    task_id = serializers.PrimaryKeyRelatedField(
        source="task",
        queryset=Task.objects.all(),
        required=False,
        allow_null=True,
        write_only=True,
    )
    dtcontact_id = serializers.PrimaryKeyRelatedField(
        source="dtcontact",
        queryset=DTContact.objects.all(),
        required=False,
        allow_null=True,
        write_only=True,
    )
    status_id = serializers.PrimaryKeyRelatedField(
        source="status",
        queryset=Status.objects.all(),
        required=False,
        allow_null=True,
        write_only=True,
    )
    alignment_id = serializers.PrimaryKeyRelatedField(
        source="alignment",
        queryset=Alignment.objects.all(),
        required=False,
        allow_null=True,
        write_only=True,
    )
    maturitymodel_id = serializers.PrimaryKeyRelatedField(
        source="maturitymodel",
        queryset=MaturityModel.objects.all(),
        required=False,
        allow_null=True,
        write_only=True,
    )
    keyword_ids = serializers.PrimaryKeyRelatedField(
        source="keywords",
        queryset=Keyword.objects.all(),
        many=True,
        required=False,
        write_only=True,
    )

    def validate(self, attrs):
        start_date = attrs.get(
            "start_date",
            getattr(self.instance, "start_date", None),
        )
        end_date = attrs.get(
            "end_date",
            getattr(self.instance, "end_date", None),
        )

        if start_date and end_date and end_date < start_date:
            raise serializers.ValidationError(
                {"end_date": "End date cannot be before start date."}
            )

        return attrs

    @staticmethod
    def _resolve_contact(contact_data):
        if contact_data is None:
            return None

        contact, _ = Contact.objects.get_or_create(**contact_data)
        return contact

    def create(self, validated_data):
        contact_data = validated_data.pop("contact", None)
        keywords = validated_data.pop("keywords", None)
        contact = self._resolve_contact(contact_data)
        instance = Tracker.objects.create(contact=contact, **validated_data)

        if keywords is not None:
            instance.keywords.set(keywords)

        return instance

    def update(self, instance, validated_data):
        if "contact" in validated_data:
            contact_data = validated_data.pop("contact")
            instance.contact = self._resolve_contact(contact_data)

        keywords = validated_data.pop("keywords", None)

        for attribute, value in validated_data.items():
            setattr(instance, attribute, value)

        instance.save()

        if keywords is not None:
            instance.keywords.set(keywords)

        return instance

    class Meta:
        model = Tracker
        depth = 2
        fields = "__all__"
