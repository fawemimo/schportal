# Generated by Django 4.1.4 on 2023-04-12 15:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0151_billing_course_fee"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="billing",
            name="course_fee",
        ),
    ]
