# Generated by Django 4.1.4 on 2023-03-21 08:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0077_alter_announcement_cookie_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="announcement",
            name="expiration_date",
            field=models.DateField(),
        ),
    ]
