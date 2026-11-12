from io import StringIO

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import TestCase

from .models import DeveloperAPIKey


class DeveloperAPIKeyCommandTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="command-user",
            password="test-password-123",
        )

    def test_revoke_command_disables_key_by_prefix(self):
        api_key, _raw_key = DeveloperAPIKey.issue(
            owner=self.user,
            name="Automation key",
        )
        stdout = StringIO()

        call_command(
            "revoke_developer_api_key",
            prefix=api_key.prefix,
            stdout=stdout,
        )

        api_key.refresh_from_db()
        self.assertFalse(api_key.is_active)
        self.assertIn("Revoked API key", stdout.getvalue())

    def test_revoke_command_is_idempotent(self):
        api_key, _raw_key = DeveloperAPIKey.issue(
            owner=self.user,
            name="Already revoked",
        )
        api_key.is_active = False
        api_key.save(update_fields=["is_active"])
        stdout = StringIO()

        call_command(
            "revoke_developer_api_key",
            prefix=api_key.prefix,
            stdout=stdout,
        )

        api_key.refresh_from_db()
        self.assertFalse(api_key.is_active)
        self.assertIn("already revoked", stdout.getvalue())

    def test_revoke_command_rejects_unknown_prefix(self):
        with self.assertRaisesMessage(CommandError, "API key does not exist."):
            call_command(
                "revoke_developer_api_key",
                prefix="does-not-exist",
            )
