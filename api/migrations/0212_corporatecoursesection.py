# Generated by Django 4.1.4 on 2023-04-26 07:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0211_studentbackup_student"),
    ]

    operations = [
        migrations.CreateModel(
            name="CorporateCourseSection",
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
                ("intro_text", models.TextField()),
            ],
        ),
    ]
