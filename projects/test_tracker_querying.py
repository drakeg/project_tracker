from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase

from .models import Contact, Status, Task, Tracker


class TrackerQueryTests(APITestCase):
    def setUp(self):
        user = get_user_model().objects.create_user(
            username="tracker-query-user",
            password="test-password-123",
        )
        self.client.force_authenticate(user=user)

        self.open_status = Status.objects.create(status_text="Open")
        self.closed_status = Status.objects.create(status_text="Closed")
        self.build_task = Task.objects.create(task_text="Build")
        self.review_task = Task.objects.create(task_text="Review")
        self.ada = Contact.objects.create(
            contact_fname="Ada",
            contact_lname="Lovelace",
            contact_phone="555-0100",
        )
        self.grace = Contact.objects.create(
            contact_fname="Grace",
            contact_lname="Hopper",
            contact_phone="555-0101",
        )

        self.alpha = Tracker.objects.create(
            title="Alpha Migration",
            status=self.open_status,
            task=self.build_task,
            contact=self.ada,
            start_date="2026-10-01",
            end_date="2026-10-10",
        )
        self.beta = Tracker.objects.create(
            title="Beta Review",
            status=self.closed_status,
            task=self.review_task,
            contact=self.grace,
            start_date="2026-10-15",
            end_date="2026-10-25",
        )

    def _titles(self, response):
        self.assertEqual(response.status_code, 200)
        return [item["title"] for item in response.json()]

    def test_filter_by_relationship_ids(self):
        response = self.client.get(
            "/api/projects/trackers/",
            {
                "status": self.open_status.pk,
                "task": self.build_task.pk,
                "contact": self.ada.pk,
            },
        )

        self.assertEqual(self._titles(response), ["Alpha Migration"])

    def test_filter_by_date_window(self):
        response = self.client.get(
            "/api/projects/trackers/",
            {
                "start_date_gte": "2026-10-10",
                "end_date_lte": "2026-10-31",
            },
        )

        self.assertEqual(self._titles(response), ["Beta Review"])

    def test_search_by_title(self):
        response = self.client.get(
            "/api/projects/trackers/",
            {"search": "migration"},
        )

        self.assertEqual(self._titles(response), ["Alpha Migration"])

    def test_order_by_start_date_descending(self):
        response = self.client.get(
            "/api/projects/trackers/",
            {"ordering": "-start_date"},
        )

        self.assertEqual(
            self._titles(response),
            ["Beta Review", "Alpha Migration"],
        )
