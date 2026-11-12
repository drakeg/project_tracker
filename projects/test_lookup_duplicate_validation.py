from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase

from .models import Alignment, MaturityModel, Task


class LookupDuplicateValidationTests(APITestCase):
    def setUp(self):
        user = get_user_model().objects.create_user(
            username="lookup-validation-user",
            password="test-password-123",
        )
        self.client.force_authenticate(user=user)

    def test_task_create_rejects_case_insensitive_duplicate(self):
        Task.objects.create(task_text="Build")

        response = self.client.post(
            "/api/projects/tasks/",
            {"task_text": "build"},
            format="json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["task_text"], ["Task already exists."])
        self.assertEqual(Task.objects.count(), 1)

    def test_task_update_rejects_case_insensitive_duplicate(self):
        Task.objects.create(task_text="Build")
        review = Task.objects.create(task_text="Review")

        response = self.client.patch(
            f"/api/projects/tasks/{review.pk}/",
            {"task_text": "BUILD"},
            format="json",
        )

        self.assertEqual(response.status_code, 400)
        review.refresh_from_db()
        self.assertEqual(review.task_text, "Review")

    def test_alignment_create_rejects_case_insensitive_duplicate(self):
        Alignment.objects.create(alignment_text="Strategic")

        response = self.client.post(
            "/api/projects/alignments/",
            {"alignment_text": "strategic"},
            format="json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json()["alignment_text"],
            ["Alignment already exists."],
        )
        self.assertEqual(Alignment.objects.count(), 1)

    def test_alignment_update_rejects_case_insensitive_duplicate(self):
        Alignment.objects.create(alignment_text="Strategic")
        operational = Alignment.objects.create(alignment_text="Operational")

        response = self.client.patch(
            f"/api/projects/alignments/{operational.pk}/",
            {"alignment_text": "STRATEGIC"},
            format="json",
        )

        self.assertEqual(response.status_code, 400)
        operational.refresh_from_db()
        self.assertEqual(operational.alignment_text, "Operational")

    def test_maturity_model_create_rejects_case_insensitive_duplicate(self):
        MaturityModel.objects.create(maturitymodel_text="Managed")

        response = self.client.post(
            "/api/projects/maturity-models/",
            {"maturitymodel_text": "managed"},
            format="json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json()["maturitymodel_text"],
            ["Maturity model already exists."],
        )
        self.assertEqual(MaturityModel.objects.count(), 1)

    def test_maturity_model_update_rejects_case_insensitive_duplicate(self):
        MaturityModel.objects.create(maturitymodel_text="Managed")
        optimized = MaturityModel.objects.create(maturitymodel_text="Optimized")

        response = self.client.patch(
            f"/api/projects/maturity-models/{optimized.pk}/",
            {"maturitymodel_text": "MANAGED"},
            format="json",
        )

        self.assertEqual(response.status_code, 400)
        optimized.refresh_from_db()
        self.assertEqual(optimized.maturitymodel_text, "Optimized")
