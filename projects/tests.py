from django.test import TestCase
from rest_framework.test import APITestCase

from .models import Keyword, Status, Task


class ModelStringTests(TestCase):
    def test_status_string(self):
        status = Status(status_text="In Progress")
        self.assertEqual(str(status), "In Progress")

    def test_task_string(self):
        task = Task(task_text="Build")
        self.assertEqual(str(task), "Build")

    def test_keyword_string(self):
        keyword = Keyword(keyword_text="django")
        self.assertEqual(str(keyword), "django")


class ApiSmokeTests(APITestCase):
    def test_status_list(self):
        Status.objects.create(status_text="Open")

        response = self.client.get("/api/projects/status/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [{"status_text": "Open"}])

    def test_keyword_list(self):
        Keyword.objects.create(keyword_text="security")

        response = self.client.get("/api/projects/keywords/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [{"keyword_text": "security"}])

    def test_empty_tracker_list(self):
        response = self.client.get("/api/projects/trackers/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])
