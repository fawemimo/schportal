# Generated by Django 4.1.4 on 2023-03-08 09:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0057_student_date_of_birth_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="batch",
            name="students",
            field=models.ManyToManyField(blank=True, null=True, to="api.student"),
        ),
    ]
