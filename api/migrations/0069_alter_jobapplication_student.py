# Generated by Django 4.1.4 on 2023-03-18 10:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0068_alter_job_job_responsibilities"),
    ]

    operations = [
        migrations.AlterField(
            model_name="jobapplication",
            name="student",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="api.student"
            ),
        ),
    ]
