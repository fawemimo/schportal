# Generated by Django 4.1.4 on 2023-03-27 15:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0090_remove_billingdetail_outstanding_amount_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="billingdetail",
            name="amount_paid",
        ),
    ]
