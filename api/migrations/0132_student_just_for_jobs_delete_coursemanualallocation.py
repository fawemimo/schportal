# Generated by Django 4.1.4 on 2023-04-11 12:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0131_rename_course_manual_batch_course_manuals"),
    ]

    operations = [
        migrations.AddField(
            model_name="student",
            name="just_for_jobs",
            field=models.BooleanField(default=False),
        ),
        migrations.DeleteModel(
            name="CourseManualAllocation",
        ),
    ]