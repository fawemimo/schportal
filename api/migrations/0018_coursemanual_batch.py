# Generated by Django 4.1.4 on 2023-01-17 10:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0017_rename_student_id_student_student_idcard_id_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="coursemanual",
            name="batch",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="api.batch",
            ),
        ),
    ]
