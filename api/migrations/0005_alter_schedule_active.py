# Generated by Django 4.1.4 on 2022-12-26 22:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_remove_course_last_updated_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schedule',
            name='active',
            field=models.BooleanField(default=False),
        ),
    ]
