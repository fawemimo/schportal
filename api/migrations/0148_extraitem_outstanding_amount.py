# Generated by Django 4.1.4 on 2023-04-12 13:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0147_remove_billing_course_billing_schedule_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="extraitem",
            name="outstanding_amount",
            field=models.CharField(default=0, max_length=50),
        ),
    ]
