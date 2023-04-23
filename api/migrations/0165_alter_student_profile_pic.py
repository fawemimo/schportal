# Generated by Django 4.1.4 on 2023-04-13 10:36

import django.core.validators
from django.db import migrations, models

import api.validate


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0164_student_is_approved"),
    ]

    operations = [
        migrations.AlterField(
            model_name="student",
            name="profile_pic",
            field=models.ImageField(
                blank=True,
                null=True,
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