# Generated by Django 4.1.4 on 2023-04-04 08:08

import tinymce.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0114_jobapplication_applied"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="job",
            options={"ordering": ["-id"]},
        ),
        migrations.AlterField(
            model_name="job",
            name="job_summary",
            field=tinymce.models.HTMLField(),
        ),
    ]
