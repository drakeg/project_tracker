"""Issue developer API keys from the command line."""

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError

from projects.models import DeveloperAPIKey


class Command(BaseCommand):
    help = "Issue a developer API key. The plaintext key is displayed once."

    def add_arguments(self, parser):
        parser.add_argument("--username", required=True)
        parser.add_argument("--name", required=True)
        parser.add_argument(
            "--plan",
            choices=[choice for choice, _label in DeveloperAPIKey.Plan.choices],
            default=DeveloperAPIKey.Plan.FREE,
        )

    def handle(self, *args, **options):
        user_model = get_user_model()
        try:
            owner = user_model.objects.get(username=options["username"])
        except user_model.DoesNotExist as exc:
            raise CommandError("User does not exist.") from exc

        api_key, raw_key = DeveloperAPIKey.issue(
            owner=owner,
            name=options["name"],
            plan=options["plan"],
        )

        self.stdout.write(
            self.style.SUCCESS(
                f"Issued {api_key.plan} API key '{api_key.name}' "
                f"for {owner.get_username()}."
            )
        )
        self.stdout.write("Store this key securely; it will not be shown again:")
        self.stdout.write(raw_key)
