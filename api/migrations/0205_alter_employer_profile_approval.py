# Generated by Django 4.1.4 on 2023-04-20 06:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0204_remove_job_save_as_job_posting_approval"),
    ]

    operations = [
        migrations.AlterField(
            model_name="employer",
            name="profile_approval",
            field=models.BooleanField(default=False),
        ),
    ]
