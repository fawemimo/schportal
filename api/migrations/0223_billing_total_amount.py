# Generated by Django 4.1.4 on 2023-05-03 14:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0222_remove_billingextrapayment_billing_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="billing",
            name="total_amount",
            field=models.PositiveBigIntegerField(blank=True, null=True),
        ),
    ]
