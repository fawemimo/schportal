# Generated by Django 4.1.4 on 2023-05-02 23:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0213_remove_billingdetail_course_fee"),
    ]

    operations = [
        migrations.AlterField(
            model_name="billingdetail",
            name="outstanding_amount",
            field=models.PositiveBigIntegerField(blank=True, null=True),
        ),
    ]
