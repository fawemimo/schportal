# Generated by Django 4.1.4 on 2023-03-31 07:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0107_blogpost_user"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="student",
            name="billings",
        ),
    ]
