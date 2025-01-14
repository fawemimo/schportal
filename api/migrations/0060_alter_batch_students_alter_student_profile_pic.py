# Generated by Django 4.1.4 on 2023-03-09 13:06

import django.core.validators
from django.db import migrations, models

import api.validate


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0059_remove_coursemanualallocation_student_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="batch",
            name="students",
            field=models.ManyToManyField(blank=True, to="api.student"),
        ),
        migrations.AlterField(
            model_name="student",
            name="profile_pic",
            field=models.ImageField(
                upload_to="students_profilepix/",
                validators=[
                    api.validate.validate_file_size,
                    django.core.validators.FileExtensionValidator(
                        allowed_extensions=["jpg", "png", "jpeg"]
                    ),
                ],
            ),
        ),
    ]
