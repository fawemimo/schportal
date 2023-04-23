# Generated by Django 4.1.4 on 2023-04-05 10:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0117_rename_interestedform_enrollment"),
    ]

    operations = [
        migrations.AddField(
            model_name="batch",
            name="program_type",
            field=models.CharField(
                blank=True,
                choices=[("Onsite", "Onsite"), ("Virtual", "Virtual")],
                max_length=50,
                null=True,
            ),
        ),
    ]