# Generated by Django 4.1.4 on 2023-04-13 08:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0161_alter_batch_course_manuals"),
    ]

    operations = [
        migrations.AlterField(
            model_name="batch",
            name="course_manuals",
            field=models.ManyToManyField(blank=True, to="api.coursemanual"),
        ),
    ]
