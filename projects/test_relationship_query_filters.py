from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase

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


class RelationshipQueryFilterTests(APITestCase):
    def setUp(self):
        user = get_user_model().objects.create_user(
            username="relationship-query-user",
            password="test-password-123",
        )
        self.client.force_authenticate(user=user)

        self.open_status = Status.objects.create(status_text="Open")
        self.build_task = Task.objects.create(task_text="Build")
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
        self.delivery = DTContact.objects.create(
            dtcontact_fname="Katherine",
            dtcontact_lname="Johnson",
            dtcontact_phone="555-0102",
        )
        self.strategic = Alignment.objects.create(
            alignment_text="Strategic",
        )
        self.managed = MaturityModel.objects.create(
            maturitymodel_text="Managed",
        )
        self.security = Keyword.objects.create(keyword_text="security")
        self.api = Keyword.objects.create(keyword_text="api")

        self.alpha = Tracker.objects.create(
            title="Alpha Migration",
            status=self.open_status,
            task=self.build_task,
            contact=self.ada,
            dtcontact=self.delivery,
            alignment=self.strategic,
            maturitymodel=self.managed,
            start_date="2026-10-01",
            end_date="2026-10-15",
        )
        self.alpha.keywords.set([self.security, self.api])

        self.beta = Tracker.objects.create(
            title="Beta Cleanup",
            contact=self.grace,
            start_date="2026-10-20",
            end_date="2026-10-30",
        )
        self.beta.keywords.set([self.api])

        Comment.objects.create(
            comment_date="2026-10-05",
            comment_text="Migration started",
            comment_user=self.ada,
            comment_tracker=self.alpha,
        )
        Comment.objects.create(
            comment_date="2026-10-25",
            comment_text="Cleanup reviewed",
            comment_user=self.grace,
            comment_tracker=self.beta,
        )

        Update.objects.create(
            update_date="2026-10-06",
            update_text="Migration reached phase two",
            update_user=self.ada,
            update_tracker=self.alpha,
        )
        Update.objects.create(
            update_date="2026-10-26",
            update_text="Cleanup completed",
            update_user=self.grace,
            update_tracker=self.beta,
        )

    def _titles(self, response):
        self.assertEqual(response.status_code, 200)
        return [item["title"] for item in response.json()["results"]]

    def test_tracker_filters_cover_all_relationships(self):
        query_cases = {
            "dtcontact": self.delivery.pk,
            "alignment": self.strategic.pk,
            "maturitymodel": self.managed.pk,
            "keyword": self.security.pk,
        }

        for parameter, value in query_cases.items():
            with self.subTest(parameter=parameter):
                response = self.client.get(
                    "/api/projects/trackers/",
                    {parameter: value},
                )
                self.assertEqual(self._titles(response), ["Alpha Migration"])

    def test_keyword_filter_does_not_duplicate_trackers(self):
        response = self.client.get(
            "/api/projects/trackers/",
            {"keyword": self.api.pk},
        )

        self.assertEqual(
            self._titles(response),
            ["Alpha Migration", "Beta Cleanup"],
        )

    def test_comment_filters_search_and_ordering(self):
        response = self.client.get(
            "/api/projects/comments/",
            {
                "tracker": self.alpha.pk,
                "user": self.ada.pk,
                "date_gte": "2026-10-01",
                "date_lte": "2026-10-10",
                "search": "started",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            [item["comment_text"] for item in response.json()["results"]],
            ["Migration started"],
        )

        ordered = self.client.get("/api/projects/comments/")
        self.assertEqual(
            [item["comment_text"] for item in ordered.json()["results"]],
            ["Cleanup reviewed", "Migration started"],
        )

    def test_update_filters_search_and_ordering(self):
        response = self.client.get(
            "/api/projects/updates/",
            {
                "tracker": self.alpha.pk,
                "user": self.ada.pk,
                "date_gte": "2026-10-01",
                "date_lte": "2026-10-10",
                "search": "phase two",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            [item["update_text"] for item in response.json()["results"]],
            ["Migration reached phase two"],
        )

        ordered = self.client.get("/api/projects/updates/")
        self.assertEqual(
            [item["update_text"] for item in ordered.json()["results"]],
            ["Cleanup completed", "Migration reached phase two"],
        )
