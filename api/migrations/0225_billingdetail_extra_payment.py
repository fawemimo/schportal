# Generated by Django 4.1.4 on 2023-05-04 08:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0224_remove_billingdetail_outstanding_amount"),
    ]

    operations = [
        migrations.AddField(
            model_name="billingdetail",
            name="extra_payment",
            field=models.BooleanField(default=False),
        ),
    ]
