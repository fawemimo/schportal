# Generated by Django 4.1.4 on 2023-05-03 02:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0219_alter_billingextrapayment_outstanding_amount"),
    ]

    operations = [
        migrations.CreateModel(
            name="BillingExtraNameAndAmount",
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
                ("item_name_fee", models.PositiveIntegerField(blank=True, null=True)),
                ("date_created", models.DateTimeField(auto_now_add=True)),
                ("date_updated", models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.RemoveField(
            model_name="billingextrapayment",
            name="item_name",
        ),
        migrations.RemoveField(
            model_name="billingextrapayment",
            name="item_name_fee",
        ),
    ]
