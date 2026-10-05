"""Serializers for the project tracker API."""

from rest_framework import serializers

from .models import Contact, Keyword, Status, Tracker


class StatusSerializer(serializers.ModelSerializer):
    """Serializer for project status values."""

    class Meta:
        model = Status
        fields = ["status_text"]


class KeywordSerializer(serializers.ModelSerializer):
    """Serializer for project keywords."""

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
    """Full tracker representation with writable nested contact data."""

    contact = RelatedContactSerializer(required=False, allow_null=True)

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
        contact = self._resolve_contact(contact_data)
        return Tracker.objects.create(contact=contact, **validated_data)

    def update(self, instance, validated_data):
        if "contact" in validated_data:
            contact_data = validated_data.pop("contact")
            instance.contact = self._resolve_contact(contact_data)

        for attribute, value in validated_data.items():
            setattr(instance, attribute, value)

        instance.save()
        return instance

    class Meta:
        model = Tracker
        depth = 2
        fields = "__all__"
