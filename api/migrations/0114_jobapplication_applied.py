# Generated by Django 4.1.4 on 2023-04-04 07:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0113_alter_jobapplication_unique_together"),
    ]

    operations = [
        migrations.AddField(
            model_name="jobapplication",
            name="applied",
            field=models.BooleanField(default=False),
        ),
    ]