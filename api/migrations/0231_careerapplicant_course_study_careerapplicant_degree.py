# Generated by Django 4.1.4 on 2023-05-15 10:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0230_billing_program_type"),
    ]

    operations = [
        migrations.AddField(
            model_name="careerapplicant",
            name="course_study",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="careerapplicant",
            name="degree",
            field=models.CharField(
                blank=True,
                choices=[
                    ("First Class", "First Class"),
                    ("Second Class Upper", "Second Class Upper"),
                    ("Second Class Lower", "Second Class Lower"),
                ],
                max_length=50,
                null=True,
            ),
        ),
    ]
