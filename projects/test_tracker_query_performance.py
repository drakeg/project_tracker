from django.contrib.auth import get_user_model
from django.db import connection
from django.test.utils import CaptureQueriesContext
from rest_framework.test import APITestCase

from .models import Contact, Keyword, Status, Task, Tracker


class TrackerQueryPerformanceTests(APITestCase):
    def setUp(self):
        user = get_user_model().objects.create_user(
            username="tracker-performance-user",
            password="test-password-123",
        )
        self.client.force_authenticate(user=user)

        status = Status.objects.create(status_text="Open")
        task = Task.objects.create(task_text="Build")
        contact = Contact.objects.create(
            contact_fname="Ada",
            contact_lname="Lovelace",
            contact_phone="555-0100",
        )
        keyword = Keyword.objects.create(keyword_text="performance")

        for index in range(20):
            tracker = Tracker.objects.create(
                title=f"Tracker {index:02d}",
                status=status,
                task=task,
                contact=contact,
            )
            tracker.keywords.add(keyword)

    def test_tracker_list_avoids_relationship_n_plus_one_queries(self):
        with CaptureQueriesContext(connection) as queries:
            response = self.client.get(
                "/api/projects/trackers/",
                {"page_size": 20},
            )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["count"], 20)
        self.assertLessEqual(len(queries), 4)
