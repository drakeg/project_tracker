"""Revoke developer API keys from the command line."""

from django.core.management.base import BaseCommand, CommandError

from projects.models import DeveloperAPIKey


class Command(BaseCommand):
    help = "Revoke a developer API key by its non-secret prefix."

    def add_arguments(self, parser):
        parser.add_argument("--prefix", required=True)

    def handle(self, *args, **options):
        prefix = options["prefix"]

        try:
            api_key = DeveloperAPIKey.objects.select_related("owner").get(
                prefix=prefix
            )
        except DeveloperAPIKey.DoesNotExist as exc:
            raise CommandError("API key does not exist.") from exc

        if not api_key.is_active:
            self.stdout.write(
                f"API key '{api_key.name}' ({api_key.prefix}) is already revoked."
            )
            return

        api_key.is_active = False
        api_key.save(update_fields=["is_active"])

        self.stdout.write(
            self.style.SUCCESS(
                f"Revoked API key '{api_key.name}' ({api_key.prefix}) "
                f"for {api_key.owner.get_username()}."
            )
        )
