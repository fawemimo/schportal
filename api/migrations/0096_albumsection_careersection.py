# Generated by Django 4.1.4 on 2023-03-28 07:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0095_alter_student_contact_address_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="AlbumSection",
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
                ("is_published", models.BooleanField(default=False)),
                ("album_photo", models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name="CareerSection",
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
                ("is_published", models.BooleanField(default=False)),
                ("intro_banner", models.TextField()),
                ("our_story", models.TextField()),
                ("mission_values", models.TextField()),
                ("team_description", models.TextField()),
            ],
        ),
    ]
