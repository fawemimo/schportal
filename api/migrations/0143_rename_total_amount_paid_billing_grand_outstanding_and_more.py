# Generated by Django 4.1.4 on 2023-04-12 12:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0142_remove_billing_email_remove_billing_first_name_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="billing",
            old_name="total_amount_paid",
            new_name="grand_outstanding",
        ),
        migrations.RemoveField(
            model_name="billing",
            name="total_amount",
        ),
        migrations.AddField(
            model_name="billing",
            name="grand_total",
            field=models.PositiveBigIntegerField(blank=True, null=True),
        ),
    ]
