# Generated by Django 4.1.4 on 2023-03-20 12:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0070_billing_billingdetail"),
    ]

    operations = [
        migrations.AlterField(
            model_name="billing",
            name="outstanding_amount",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
