# Generated by Django 4.1.4 on 2023-04-12 08:38

import django.core.validators
from django.db import migrations, models

import api.validate


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0138_alter_billingdetail_outstanding_amount"),
    ]

    operations = [
        migrations.CreateModel(
            name="ExtraItem",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("item_name", models.CharField(max_length=255)),
                ("amount_paid", models.PositiveIntegerField()),
                ("date_created", models.DateTimeField(auto_now_add=True)),
                ("date_updated", models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.AlterField(
            model_name="billingdetail",
            name="outstanding_amount",
            field=models.CharField(default=0, max_length=50),
        ),
        migrations.AlterField(
            model_name="employer",
            name="company_logo",
            field=models.ImageField(
                default="JobPortal/Company/c.png",
                upload_to="JobPortal/Company",
                validators=[
                    api.validate.validate_file_size,
                    django.core.validators.FileExtensionValidator(
                        allowed_extensions=["svg", "jpg", "png", "jpeg"]
                    ),
                ],
            ),
        ),
    ]
