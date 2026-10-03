# Generated for the current project_tracker model schema.

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Alignment",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("alignment_text", models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name="Contact",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("contact_fname", models.CharField(max_length=50)),
                ("contact_lname", models.CharField(max_length=50)),
                ("contact_email", models.EmailField(max_length=254, null=True)),
                ("contact_username", models.CharField(max_length=50, null=True)),
                ("contact_phone", models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name="DTContact",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("dtcontact_fname", models.CharField(max_length=50)),
                ("dtcontact_lname", models.CharField(max_length=50)),
                ("dtcontact_phone", models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name="Keyword",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("keyword_text", models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name="MaturityModel",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("maturitymodel_text", models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name="Status",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("status_text", models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name="Task",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("task_text", models.CharField(max_length=25)),
            ],
        ),
        migrations.CreateModel(
            name="Tracker",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=100)),
                ("start_date", models.DateField(blank=True, null=True, verbose_name="date_started")),
                ("end_date", models.DateField(blank=True, null=True, verbose_name="date_ended")),
                ("create_date", models.DateField(auto_now_add=True)),
                (
                    "alignment",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="projects.alignment",
                    ),
                ),
                (
                    "contact",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="projects.contact",
                    ),
                ),
                (
                    "dtcontact",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="projects.dtcontact",
                    ),
                ),
                (
                    "keywords",
                    models.ManyToManyField(blank=True, to="projects.keyword"),
                ),
                (
                    "maturitymodel",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="projects.maturitymodel",
                    ),
                ),
                (
                    "status",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="projects.status",
                    ),
                ),
                (
                    "task",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="projects.task",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Update",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("update_date", models.DateField()),
                ("update_text", models.CharField(max_length=150)),
                (
                    "update_tracker",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="projects.tracker",
                    ),
                ),
                (
                    "update_user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="projects.contact",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Comment",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("comment_date", models.DateField()),
                ("comment_text", models.CharField(max_length=200)),
                (
                    "comment_tracker",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="projects.tracker",
                    ),
                ),
                (
                    "comment_user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="projects.contact",
                    ),
                ),
            ],
        ),
    ]
