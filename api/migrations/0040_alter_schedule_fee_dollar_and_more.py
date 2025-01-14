# Generated by Django 4.1.4 on 2023-02-09 11:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0039_alter_schedule_naira_to_dollar_rate"),
    ]

    operations = [
        migrations.AlterField(
            model_name="schedule",
            name="fee_dollar",
            field=models.IntegerField(blank=True, default=0, editable=False, null=True),
        ),
        migrations.AlterField(
            model_name="schedule",
            name="naira_to_dollar_rate",
            field=models.DecimalField(
                blank=True, decimal_places=2, default=0, max_digits=6, null=True
            ),
        ),
    ]
