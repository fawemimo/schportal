# Generated by Django 4.1.4 on 2023-04-18 14:51

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0193_rename_intro_banner_careersection_find_your_role_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="CareerCategory",
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
                ("title", models.CharField(max_length=255)),
                ("description", models.TextField()),
                ("date_created", models.DateTimeField(auto_now_add=True)),
                ("date_updated", models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name="CareerOpening",
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
                ("title", models.CharField(max_length=255)),
                ("description", models.TextField()),
                (
                    "career_category",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="api.careercategory",
                    ),
                ),
                (
                    "employment_type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="api.jobtype"
                    ),
                ),
                (
                    "job_location",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="api.joblocation",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="CareerApplicant",
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
                ("first_name", models.CharField(max_length=255)),
                ("last_name", models.CharField(max_length=255)),
                ("email", models.EmailField(max_length=255, unique=True)),
                ("mobile", models.CharField(max_length=255)),
                (
                    "resume",
                    models.FileField(
                        blank=True,
                        null=True,
                        upload_to="career/applicant/",
                        validators=[
                            django.core.validators.FileExtensionValidator(
                                allowed_extensions=["pdf"]
                            )
                        ],
                    ),
                ),
                ("date_created", models.DateTimeField(auto_now_add=True)),
                ("date_updated", models.DateTimeField(auto_now=True)),
                (
                    "career_opening",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="api.careeropening",
                    ),
                ),
            ],
        ),
    ]
