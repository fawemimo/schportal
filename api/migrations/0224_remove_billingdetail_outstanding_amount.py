# Generated by Django 4.1.4 on 2023-05-03 14:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0223_billing_total_amount"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="billingdetail",
            name="outstanding_amount",
        ),
    ]
