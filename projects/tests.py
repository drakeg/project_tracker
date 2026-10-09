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

    def test_status_create_rejects_case_insensitive_duplicate(self):
        Status.objects.create(status_text="Open")

        response = self.client.post(
            "/api/projects/status/",
            {"status_text": "open"},
            format="json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["status_text"], ["Status already exists."])
        self.assertEqual(Status.objects.count(), 1)

    def test_status_crud(self):
        create_response = self.client.post(
            "/api/projects/status/",
            {"status_text": "Blocked"},
            format="json",
        )
        self.assertEqual(create_response.status_code, 201)

        status = Status.objects.get(status_text="Blocked")
        update_response = self.client.patch(
            f"/api/projects/status/{status.pk}/",
            {"status_text": "Waiting"},
            format="json",
        )
        self.assertEqual(update_response.status_code, 200)

        delete_response = self.client.delete(f"/api/projects/status/{status.pk}/")
        self.assertEqual(delete_response.status_code, 204)
        self.assertFalse(Status.objects.filter(pk=status.pk).exists())

    def test_status_update_rejects_case_insensitive_duplicate(self):
        Status.objects.create(status_text="Open")
        blocked = Status.objects.create(status_text="Blocked")

        response = self.client.patch(
            f"/api/projects/status/{blocked.pk}/",
            {"status_text": "OPEN"},
            format="json",
        )

        self.assertEqual(response.status_code, 400)
        blocked.refresh_from_db()
        self.assertEqual(blocked.status_text, "Blocked")

    def test_keyword_list(self):
        Keyword.objects.create(keyword_text="security")

        response = self.client.get("/api/projects/keywords/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [{"keyword_text": "security"}])

    def test_keyword_create_rejects_case_insensitive_duplicate(self):
        Keyword.objects.create(keyword_text="security")

        response = self.client.post(
            "/api/projects/keywords/",
            {"keyword_text": "SECURITY"},
            format="json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["keyword_text"], ["Keyword already exists."])
        self.assertEqual(Keyword.objects.count(), 1)

    def test_keyword_crud(self):
        create_response = self.client.post(
            "/api/projects/keywords/",
            {"keyword_text": "api"},
            format="json",
        )
        self.assertEqual(create_response.status_code, 201)

        keyword = Keyword.objects.get(keyword_text="api")
        update_response = self.client.patch(
            f"/api/projects/keywords/{keyword.pk}/",
            {"keyword_text": "rest"},
            format="json",
        )
        self.assertEqual(update_response.status_code, 200)

        delete_response = self.client.delete(f"/api/projects/keywords/{keyword.pk}/")
        self.assertEqual(delete_response.status_code, 204)
        self.assertFalse(Keyword.objects.filter(pk=keyword.pk).exists())

    def test_keyword_update_rejects_case_insensitive_duplicate(self):
        Keyword.objects.create(keyword_text="security")
        api_keyword = Keyword.objects.create(keyword_text="api")

        response = self.client.patch(
            f"/api/projects/keywords/{api_keyword.pk}/",
            {"keyword_text": "Security"},
            format="json",
        )

        self.assertEqual(response.status_code, 400)
        api_keyword.refresh_from_db()
        self.assertEqual(api_keyword.keyword_text, "api")

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

    def test_tracker_create_rejects_end_before_start(self):
        response = self.client.post(
            "/api/projects/trackers/",
            {
                "title": "Invalid dates",
                "start_date": "2026-10-10",
                "end_date": "2026-10-09",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json()["end_date"],
            ["End date cannot be before start date."],
        )
        self.assertFalse(Tracker.objects.exists())

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

    def test_tracker_patch_rejects_invalid_date_range(self):
        tracker = Tracker.objects.create(
            title="Scheduled work",
            start_date="2026-10-10",
            end_date="2026-10-20",
        )

        response = self.client.patch(
            f"/api/projects/trackers/{tracker.pk}/",
            {"end_date": "2026-10-09"},
            format="json",
        )

        self.assertEqual(response.status_code, 400)
        tracker.refresh_from_db()
        self.assertEqual(str(tracker.end_date), "2026-10-20")

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
