# Generated by Django 4.1.4 on 2023-04-22 10:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0209_alter_employer_options_alter_employer_date_updated"),
    ]

    operations = [
        migrations.AlterField(
            model_name="job",
            name="posting_approval",
            field=models.BooleanField(default=False),
        ),
    ]