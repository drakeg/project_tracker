from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase

from .models import Status


class ApiPaginationTests(APITestCase):
    def setUp(self):
        user = get_user_model().objects.create_user(
            username="pagination-user",
            password="test-password-123",
        )
        self.client.force_authenticate(user=user)

        Status.objects.bulk_create(
            [Status(status_text=f"Status {index:02d}") for index in range(55)]
        )

    def test_default_page_size_and_navigation(self):
        first_page = self.client.get("/api/projects/status/")

        self.assertEqual(first_page.status_code, 200)
        payload = first_page.json()
        self.assertEqual(payload["count"], 55)
        self.assertEqual(len(payload["results"]), 50)
        self.assertIsNotNone(payload["next"])
        self.assertIsNone(payload["previous"])

        second_page = self.client.get("/api/projects/status/", {"page": 2})
        second_payload = second_page.json()
        self.assertEqual(len(second_payload["results"]), 5)
        self.assertIsNone(second_payload["next"])
        self.assertIsNotNone(second_payload["previous"])

    def test_client_can_request_smaller_page_size(self):
        response = self.client.get(
            "/api/projects/status/",
            {"page_size": 10},
        )

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["count"], 55)
        self.assertEqual(len(payload["results"]), 10)
        self.assertIsNotNone(payload["next"])
