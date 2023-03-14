# Generated by Django 4.1.4 on 2023-03-14 02:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0061_employer_job_jobcategory_jobapplication_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="jobapplication",
            name="student",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="api.student",
            ),
        ),
    ]
