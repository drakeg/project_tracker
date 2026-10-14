"""Authentication for developer API keys."""

from django.utils import timezone
from rest_framework import authentication, exceptions

from .models import DeveloperAPIKey


class DeveloperAPIKeyAuthentication(authentication.BaseAuthentication):
    """Authenticate requests carrying an X-API-Key header."""

    header_name = "X-API-Key"

    def authenticate(self, request):
        raw_key = request.headers.get(self.header_name)
        if not raw_key:
            return None

        try:
            marker, prefix, _secret = raw_key.split("_", 2)
        except ValueError as exc:
            raise exceptions.AuthenticationFailed("Invalid API key.") from exc

        if marker != "ptk":
            raise exceptions.AuthenticationFailed("Invalid API key.")

        try:
            api_key = DeveloperAPIKey.objects.select_related("owner").get(
                prefix=prefix,
                is_active=True,
            )
        except DeveloperAPIKey.DoesNotExist as exc:
            raise exceptions.AuthenticationFailed("Invalid API key.") from exc

        if api_key.expires_at and api_key.expires_at <= timezone.now():
            raise exceptions.AuthenticationFailed("Invalid API key.")

        if not api_key.matches(raw_key):
            raise exceptions.AuthenticationFailed("Invalid API key.")

        if not api_key.owner.is_active:
            raise exceptions.AuthenticationFailed("Invalid API key.")

        return api_key.owner, api_key

    def authenticate_header(self, request):
        return self.header_name
