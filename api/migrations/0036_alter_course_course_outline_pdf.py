# Generated by Django 4.1.4 on 2023-02-08 08:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0035_rename_active_course_published"),
    ]

    operations = [
        migrations.AlterField(
            model_name="course",
            name="course_outline_pdf",
            field=models.FileField(blank=True, null=True, upload_to=""),
        ),
    ]
