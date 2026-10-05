from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APITestCase

from .models import Contact, Keyword, Status, Task, Tracker


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

    def test_contact_string_uses_username_when_present(self):
        contact = Contact(
            contact_fname="Ada",
            contact_lname="Lovelace",
            contact_phone="555-0100",
            contact_username="ada",
        )
        self.assertEqual(str(contact), "ada")

    def test_contact_string_falls_back_to_name(self):
        contact = Contact(
            contact_fname="Ada",
            contact_lname="Lovelace",
            contact_phone="555-0100",
        )
        self.assertEqual(str(contact), "Lovelace, Ada")


class AnonymousApiAccessTests(APITestCase):
    def test_project_api_requires_authentication(self):
        response = self.client.get("/api/projects/trackers/")

        self.assertEqual(response.status_code, 401)

    def test_openapi_schema_remains_public(self):
        response = self.client.get("/api/schema/")

        self.assertEqual(response.status_code, 200)

    def test_swagger_ui_remains_public(self):
        response = self.client.get("/api/docs/")

        self.assertEqual(response.status_code, 200)


class ApiSmokeTests(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="api-test-user",
            password="test-password-123",
        )
        self.client.force_authenticate(user=self.user)

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

    def test_openapi_schema_is_available(self):
        response = self.client.get("/api/schema/")

        self.assertEqual(response.status_code, 200)
        self.assertIn("openapi:", response.content.decode())
        self.assertIn("/api/projects/trackers/", response.content.decode())

    def test_swagger_ui_is_available(self):
        response = self.client.get("/api/docs/")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "SwaggerUIBundle")
        self.assertContains(response, "/api/schema/")

    def test_tracker_create_with_nested_contact(self):
        response = self.client.post(
            "/api/projects/trackers/",
            {
                "title": "Modernize API",
                "contact": {
                    "contact_fname": "Ada",
                    "contact_lname": "Lovelace",
                    "contact_phone": "555-0100",
                },
            },
            format="json",
        )

        self.assertEqual(response.status_code, 201)
        tracker = Tracker.objects.get()
        self.assertEqual(tracker.title, "Modernize API")
        self.assertEqual(tracker.contact.contact_lname, "Lovelace")
        self.assertEqual(Contact.objects.count(), 1)

    def test_tracker_patch_updates_nested_contact(self):
        original_contact = Contact.objects.create(
            contact_fname="Grace",
            contact_lname="Hopper",
            contact_phone="555-0101",
        )
        tracker = Tracker.objects.create(
            title="Initial title",
            contact=original_contact,
        )

        response = self.client.patch(
            f"/api/projects/trackers/{tracker.pk}/",
            {
                "title": "Updated title",
                "contact": {
                    "contact_fname": "Ada",
                    "contact_lname": "Lovelace",
                    "contact_phone": "555-0100",
                },
            },
            format="json",
        )

        self.assertEqual(response.status_code, 200)
        tracker.refresh_from_db()
        self.assertEqual(tracker.title, "Updated title")
        self.assertEqual(tracker.contact.contact_lname, "Lovelace")
        self.assertEqual(Contact.objects.count(), 2)

    def test_tracker_patch_can_clear_contact(self):
        contact = Contact.objects.create(
            contact_fname="Grace",
            contact_lname="Hopper",
            contact_phone="555-0101",
        )
        tracker = Tracker.objects.create(title="Contact cleanup", contact=contact)

        response = self.client.patch(
            f"/api/projects/trackers/{tracker.pk}/",
            {"contact": None},
            format="json",
        )

        self.assertEqual(response.status_code, 200)
        tracker.refresh_from_db()
        self.assertIsNone(tracker.contact)
