# Generated by Django 4.1.4 on 2023-03-28 03:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0094_remove_billing_outstanding_amount_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="student",
            name="contact_address",
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name="student",
            name="mobile_numbers",
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name="student",
            name="next_of_kin_contact_address",
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name="student",
            name="next_of_kin_fullname",
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name="student",
            name="residential_address",
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]
