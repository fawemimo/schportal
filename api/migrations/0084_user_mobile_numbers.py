# Generated by Django 4.1.4 on 2023-03-22 10:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0083_remove_billing_date_paid_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="mobile_numbers",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]