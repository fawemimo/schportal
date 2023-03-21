# Generated by Django 4.1.4 on 2023-03-21 08:25

import uuid

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0076_announcement_cookie_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="announcement",
            name="cookie_id",
            field=models.UUIDField(
                blank=True, default=uuid.uuid4, null=True, unique=True
            ),
        ),
    ]
