# Generated by Django 4.1.4 on 2023-03-28 13:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0102_financialaid_course"),
    ]

    operations = [
        migrations.RenameField(
            model_name="internationalmodel",
            old_name="intro_txt",
            new_name="why_choose_virtual",
        ),
    ]