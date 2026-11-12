from django.contrib import admin
from django.test import SimpleTestCase

from .admin import CommentAdmin, ContactAdmin, DTContactAdmin, TrackerAdmin, UpdateAdmin
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


class AdminConfigurationTests(SimpleTestCase):
    def test_core_models_are_registered(self):
        for model in (
            Tracker,
            Task,
            Contact,
            Status,
            Keyword,
            Update,
            Alignment,
            Comment,
            DTContact,
            MaturityModel,
        ):
            with self.subTest(model=model.__name__):
                self.assertIn(model, admin.site._registry)

    def test_tracker_admin_supports_search_filtering_and_keywords(self):
        self.assertEqual(TrackerAdmin.date_hierarchy, "create_date")
        self.assertIn("status", TrackerAdmin.list_filter)
        self.assertIn("title", TrackerAdmin.search_fields)
        self.assertEqual(TrackerAdmin.filter_horizontal, ("keywords",))

    def test_contact_admin_supports_identity_search(self):
        self.assertIn("contact_email", ContactAdmin.search_fields)
        self.assertIn("contact_phone", ContactAdmin.search_fields)

    def test_delivery_team_contact_admin_supports_search(self):
        self.assertIn("dtcontact_lname", DTContactAdmin.search_fields)
        self.assertIn("dtcontact_phone", DTContactAdmin.search_fields)

    def test_comment_admin_supports_date_navigation_and_search(self):
        self.assertEqual(CommentAdmin.date_hierarchy, "comment_date")
        self.assertIn("comment_tracker__title", CommentAdmin.search_fields)

    def test_update_admin_supports_date_navigation_and_search(self):
        self.assertEqual(UpdateAdmin.date_hierarchy, "update_date")
        self.assertIn("update_tracker__title", UpdateAdmin.search_fields)
