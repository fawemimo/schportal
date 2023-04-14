# Generated by Django 4.1.4 on 2023-04-14 04:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0169_alter_studentbackup_student"),
    ]

    operations = [
        migrations.AlterField(
            model_name="studentbackup",
            name="student",
            field=models.OneToOneField(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="api.student",
            ),
        ),
    ]
