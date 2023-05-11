# Generated by Django 4.1.4 on 2023-05-11 10:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0229_billing_total_amount_text"),
    ]

    operations = [
        migrations.AddField(
            model_name="billing",
            name="program_type",
            field=models.CharField(
                blank=True,
                choices=[("Onsite", "Onsite"), ("Virtual", "Virtual")],
                max_length=50,
                null=True,
            ),
        ),
    ]
