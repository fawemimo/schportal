# Generated by Django 4.1.4 on 2023-01-18 09:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0020_remove_coursemanual_enrollment_coursemanual_title_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="project",
            name="student",
        ),
    ]