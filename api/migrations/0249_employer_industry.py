# Generated by Django 4.1.4 on 2023-06-01 12:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0248_alter_billing_receipt_no'),
    ]

    operations = [
        migrations.AddField(
            model_name='employer',
            name='industry',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
