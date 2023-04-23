# Generated by Django 4.1.4 on 2023-04-18 09:05

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0183_album_alter_student_is_approved_and_more"),
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
                    django.core.validators.FileExtensionValidator(
                        allowed_extensions=["jpg", "jpeg", "png", "svg"]
                    )
                ],
            ),
        ),
    ]