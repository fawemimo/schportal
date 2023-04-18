# Generated by Django 4.1.4 on 2023-04-18 18:21

import api.validate
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0194_careercategory_careeropening_careerapplicant"),
    ]

    operations = [
        migrations.AlterField(
            model_name="album",
            name="image_cover",
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to="album/cover/",
                validators=[
                    api.validate.validate_file_size,
                    django.core.validators.FileExtensionValidator(
                        allowed_extensions=["jpg", "jpeg", "png", "svg"]
                    ),
                ],
            ),
        ),
        migrations.AlterField(
            model_name="albumdetail",
            name="image",
            field=models.ImageField(
                upload_to="album/details/",
                validators=[
                    api.validate.validate_file_size,
                    django.core.validators.FileExtensionValidator(
                        allowed_extensions=["jpg", "jpeg", "png", "svg"]
                    ),
                ],
            ),
        ),
        migrations.AlterField(
            model_name="careerapplicant",
            name="email",
            field=models.EmailField(max_length=255),
        ),
        migrations.AlterField(
            model_name="careerapplicant",
            name="resume",
            field=models.FileField(
                blank=True,
                null=True,
                upload_to="career/applicant/",
                validators=[
                    api.validate.validate_file_size,
                    django.core.validators.FileExtensionValidator(
                        allowed_extensions=["pdf"]
                    ),
                ],
            ),
        ),
    ]
