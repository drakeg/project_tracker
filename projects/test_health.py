from unittest.mock import patch

from django.db import DatabaseError
from django.test import TestCase


class HealthEndpointTests(TestCase):
    def test_health_reports_application_and_database_ready(self):
        response = self.client.get("/health/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                "status": "ok",
                "database": "ok",
            },
        )

    @patch("projects.health.connection.cursor")
    def test_health_returns_503_when_database_is_unavailable(self, cursor):
        cursor.side_effect = DatabaseError("database unavailable")

        response = self.client.get("/health/")

        self.assertEqual(response.status_code, 503)
        self.assertEqual(
            response.json(),
            {
                "status": "unhealthy",
                "database": "unavailable",
            },
        )
