"""Request throttles for developer API key plans."""

from django.conf import settings
from rest_framework.throttling import SimpleRateThrottle

from .models import DeveloperAPIKey


class DeveloperAPIKeyPlanThrottle(SimpleRateThrottle):
    """Base throttle that applies only to one developer API key plan."""

    plan = None

    def get_rate(self):
        """Read the current configured rate for this throttle scope."""
        return settings.REST_FRAMEWORK["DEFAULT_THROTTLE_RATES"].get(self.scope)

    def get_cache_key(self, request, view):
        api_key = request.auth
        if not isinstance(api_key, DeveloperAPIKey):
            return None
        if api_key.plan != self.plan:
            return None

        return self.cache_format % {
            "scope": self.scope,
            "ident": api_key.prefix,
        }


class FreeDeveloperAPIKeyThrottle(DeveloperAPIKeyPlanThrottle):
    """Throttle free developer API keys."""

    scope = "developer_api_free"
    plan = DeveloperAPIKey.Plan.FREE


class PaidDeveloperAPIKeyThrottle(DeveloperAPIKeyPlanThrottle):
    """Throttle developer-plan API keys."""

    scope = "developer_api_developer"
    plan = DeveloperAPIKey.Plan.DEVELOPER
