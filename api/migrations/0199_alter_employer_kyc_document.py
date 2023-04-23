# Generated by Django 4.1.4 on 2023-04-19 09:45

import django.core.validators
from django.db import migrations, models

import api.validate


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0198_employer_kyc_document"),
    ]

    operations = [
        migrations.AlterField(
            model_name="employer",
            name="kyc_document",
            field=models.FileField(
                blank=True,
                null=True,
                upload_to="JobPortal/Company",
                validators=[
                    api.validate.validate_file_size,
                    django.core.validators.FileExtensionValidator(
                        allowed_extensions=["pdf"]
                    ),
                ],
            ),
        ),
    ]