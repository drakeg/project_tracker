# Generated manually for the DeveloperAPIKey model.

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("projects", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="DeveloperAPIKey",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                (
                    "prefix",
                    models.CharField(editable=False, max_length=16, unique=True),
                ),
                ("key_hash", models.CharField(editable=False, max_length=128)),
                (
                    "plan",
                    models.CharField(
                        choices=[
                            ("free", "Free"),
                            ("developer", "Developer"),
                            ("internal", "Internal"),
                        ],
                        default="free",
                        max_length=20,
                    ),
                ),
                ("is_active", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("expires_at", models.DateTimeField(blank=True, null=True)),
                (
                    "owner",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="developer_api_keys",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
