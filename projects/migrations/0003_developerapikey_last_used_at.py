from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("projects", "0002_developerapikey"),
    ]

    operations = [
        migrations.AddField(
            model_name="developerapikey",
            name="last_used_at",
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
