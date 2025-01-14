# Generated by Django 4.1.4 on 2023-03-06 10:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0056_remove_assignment_batch_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="student",
            name="date_of_birth",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name="student",
            name="next_of_kin_mobile_number",
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AddField(
            model_name="student",
            name="relationship_with_next_kin",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
