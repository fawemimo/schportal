# Generated by Django 4.1.4 on 2023-04-12 14:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0150_remove_billingdetail_program_type"),
    ]

    operations = [
        migrations.AddField(
            model_name="billing",
            name="course_fee",
            field=models.PositiveBigIntegerField(blank=True, null=True),
        ),
    ]
