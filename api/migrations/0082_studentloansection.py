# Generated by Django 4.1.4 on 2023-03-21 11:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0081_remove_announcement_cookie_id"),
    ]

    operations = [
        migrations.CreateModel(
            name="StudentLoanSection",
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
                ("loan_intro", models.TextField()),
                ("how_it_works", models.TextField()),
                ("eligibility", models.TextField()),
            ],
        ),
    ]
