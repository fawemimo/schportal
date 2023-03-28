# Generated by Django 4.1.4 on 2023-03-28 12:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0099_remove_payment_course_delete_enrollment_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="financialaid",
            name="guarantor_full_name",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="financialaid",
            name="guarantor_mobile",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="financialaid",
            name="guarantor_residential_contact_address",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="financialaid",
            name="relationship_with_guarantor",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="financialaid",
            name="residential_address",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
