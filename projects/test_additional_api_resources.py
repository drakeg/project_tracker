from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase

from .models import Alignment, Comment, Contact, DTContact, MaturityModel, Task, Update


class AdditionalApiResourceTests(APITestCase):
    def setUp(self):
        user = get_user_model().objects.create_user(
            username="additional-api-user",
            password="test-password-123",
        )
        self.client.force_authenticate(user=user)

    def _assert_simple_crud(
        self,
        *,
        endpoint,
        model,
        create_payload,
        update_payload,
        lookup_field,
        expected_updated_value,
    ):
        create_response = self.client.post(endpoint, create_payload, format="json")
        self.assertEqual(create_response.status_code, 201)

        instance = model.objects.get()
        detail_endpoint = f"{endpoint}{instance.pk}/"

        update_response = self.client.patch(
            detail_endpoint,
            update_payload,
            format="json",
        )
        self.assertEqual(update_response.status_code, 200)

        instance.refresh_from_db()
        self.assertEqual(getattr(instance, lookup_field), expected_updated_value)

        delete_response = self.client.delete(detail_endpoint)
        self.assertEqual(delete_response.status_code, 204)
        self.assertFalse(model.objects.filter(pk=instance.pk).exists())

    def test_task_crud(self):
        self._assert_simple_crud(
            endpoint="/api/projects/tasks/",
            model=Task,
            create_payload={"task_text": "Build"},
            update_payload={"task_text": "Review"},
            lookup_field="task_text",
            expected_updated_value="Review",
        )

    def test_dtcontact_crud(self):
        self._assert_simple_crud(
            endpoint="/api/projects/dtcontacts/",
            model=DTContact,
            create_payload={
                "dtcontact_fname": "Ada",
                "dtcontact_lname": "Lovelace",
                "dtcontact_phone": "555-0100",
            },
            update_payload={"dtcontact_phone": "555-0101"},
            lookup_field="dtcontact_phone",
            expected_updated_value="555-0101",
        )

    def test_alignment_crud(self):
        self._assert_simple_crud(
            endpoint="/api/projects/alignments/",
            model=Alignment,
            create_payload={"alignment_text": "Strategic"},
            update_payload={"alignment_text": "Operational"},
            lookup_field="alignment_text",
            expected_updated_value="Operational",
        )

    def test_maturity_model_crud(self):
        self._assert_simple_crud(
            endpoint="/api/projects/maturity-models/",
            model=MaturityModel,
            create_payload={"maturitymodel_text": "Initial"},
            update_payload={"maturitymodel_text": "Managed"},
            lookup_field="maturitymodel_text",
            expected_updated_value="Managed",
        )

    def test_comment_crud_with_contact(self):
        contact = Contact.objects.create(
            contact_fname="Grace",
            contact_lname="Hopper",
            contact_phone="555-0102",
        )

        create_response = self.client.post(
            "/api/projects/comments/",
            {
                "comment_date": "2026-10-30",
                "comment_text": "Initial comment",
                "comment_user": contact.pk,
                "comment_tracker": None,
            },
            format="json",
        )
        self.assertEqual(create_response.status_code, 201)

        comment = Comment.objects.get()
        update_response = self.client.patch(
            f"/api/projects/comments/{comment.pk}/",
            {"comment_text": "Updated comment"},
            format="json",
        )
        self.assertEqual(update_response.status_code, 200)

        comment.refresh_from_db()
        self.assertEqual(comment.comment_text, "Updated comment")
        self.assertEqual(comment.comment_user, contact)

        delete_response = self.client.delete(f"/api/projects/comments/{comment.pk}/")
        self.assertEqual(delete_response.status_code, 204)
        self.assertFalse(Comment.objects.filter(pk=comment.pk).exists())

    def test_update_crud_with_contact(self):
        contact = Contact.objects.create(
            contact_fname="Katherine",
            contact_lname="Johnson",
            contact_phone="555-0103",
        )

        create_response = self.client.post(
            "/api/projects/updates/",
            {
                "update_date": "2026-10-30",
                "update_text": "Initial update",
                "update_user": contact.pk,
                "update_tracker": None,
            },
            format="json",
        )
        self.assertEqual(create_response.status_code, 201)

        update = Update.objects.get()
        patch_response = self.client.patch(
            f"/api/projects/updates/{update.pk}/",
            {"update_text": "Completed update"},
            format="json",
        )
        self.assertEqual(patch_response.status_code, 200)

        update.refresh_from_db()
        self.assertEqual(update.update_text, "Completed update")
        self.assertEqual(update.update_user, contact)

        delete_response = self.client.delete(f"/api/projects/updates/{update.pk}/")
        self.assertEqual(delete_response.status_code, 204)
        self.assertFalse(Update.objects.filter(pk=update.pk).exists())
