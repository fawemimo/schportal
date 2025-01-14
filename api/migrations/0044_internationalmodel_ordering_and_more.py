# Generated by Django 4.1.4 on 2023-02-10 10:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0043_alter_schedule_program_type"),
    ]

    operations = [
        migrations.AddField(
            model_name="internationalmodel",
            name="ordering",
            field=models.CharField(blank=True, max_length=25, null=True),
        ),
        migrations.AddField(
            model_name="schedule",
            name="discounted_fee_dollar",
            field=models.DecimalField(
                blank=True, decimal_places=2, max_digits=6, null=True
            ),
        ),
    ]
