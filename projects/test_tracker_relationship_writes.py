from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase

from .models import (
    Alignment,
    DTContact,
    Keyword,
    MaturityModel,
    Status,
    Task,
    Tracker,
)


class TrackerRelationshipWriteTests(APITestCase):
    def setUp(self):
        user = get_user_model().objects.create_user(
            username="tracker-relationship-user",
            password="test-password-123",
        )
        self.client.force_authenticate(user=user)

        self.task = Task.objects.create(task_text="Build")
        self.dtcontact = DTContact.objects.create(
            dtcontact_fname="Ada",
            dtcontact_lname="Lovelace",
            dtcontact_phone="555-0100",
        )
        self.status = Status.objects.create(status_text="Open")
        self.alignment = Alignment.objects.create(alignment_text="Strategic")
        self.maturity = MaturityModel.objects.create(
            maturitymodel_text="Managed"
        )
        self.security = Keyword.objects.create(keyword_text="security")
        self.api = Keyword.objects.create(keyword_text="api")

    def test_create_tracker_with_relationship_ids(self):
        response = self.client.post(
            "/api/projects/trackers/",
            {
                "title": "Relationship write support",
                "task_id": self.task.pk,
                "dtcontact_id": self.dtcontact.pk,
                "status_id": self.status.pk,
                "alignment_id": self.alignment.pk,
                "maturitymodel_id": self.maturity.pk,
                "keyword_ids": [self.security.pk, self.api.pk],
            },
            format="json",
        )

        self.assertEqual(response.status_code, 201)

        tracker = Tracker.objects.get()
        self.assertEqual(tracker.task, self.task)
        self.assertEqual(tracker.dtcontact, self.dtcontact)
        self.assertEqual(tracker.status, self.status)
        self.assertEqual(tracker.alignment, self.alignment)
        self.assertEqual(tracker.maturitymodel, self.maturity)
        self.assertEqual(
            set(tracker.keywords.values_list("pk", flat=True)),
            {self.security.pk, self.api.pk},
        )

        payload = response.json()
        self.assertNotIn("task_id", payload)
        self.assertNotIn("keyword_ids", payload)
        self.assertEqual(payload["task"]["task_text"], "Build")
        self.assertEqual(payload["status"]["status_text"], "Open")

    def test_patch_can_replace_and_clear_relationships(self):
        replacement_task = Task.objects.create(task_text="Review")
        tracker = Tracker.objects.create(
            title="Existing tracker",
            task=self.task,
            status=self.status,
            alignment=self.alignment,
        )
        tracker.keywords.set([self.security])

        response = self.client.patch(
            f"/api/projects/trackers/{tracker.pk}/",
            {
                "task_id": replacement_task.pk,
                "status_id": None,
                "alignment_id": None,
                "keyword_ids": [self.api.pk],
            },
            format="json",
        )

        self.assertEqual(response.status_code, 200)

        tracker.refresh_from_db()
        self.assertEqual(tracker.task, replacement_task)
        self.assertIsNone(tracker.status)
        self.assertIsNone(tracker.alignment)
        self.assertEqual(
            list(tracker.keywords.values_list("pk", flat=True)),
            [self.api.pk],
        )

    def test_unknown_relationship_id_is_rejected(self):
        response = self.client.post(
            "/api/projects/trackers/",
            {
                "title": "Invalid relationship",
                "task_id": 999999,
            },
            format="json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn("task_id", response.json())
        self.assertFalse(Tracker.objects.exists())
