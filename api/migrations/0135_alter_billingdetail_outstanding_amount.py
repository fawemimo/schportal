# Generated by Django 4.1.4 on 2023-04-11 13:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0134_alter_billingdetail_outstanding_amount"),
    ]

    operations = [
        migrations.AlterField(
            model_name="billingdetail",
            name="outstanding_amount",
            field=models.PositiveBigIntegerField(blank=True, default=0, null=True),
        ),
    ]