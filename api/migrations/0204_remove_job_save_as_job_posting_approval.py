# Generated by Django 4.1.4 on 2023-04-19 13:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0203_rename_posting_approval_employer_profile_approval"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="job",
            name="save_as",
        ),
        migrations.AddField(
            model_name="job",
            name="posting_approval",
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
