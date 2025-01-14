# Generated by Django 4.1.4 on 2023-01-19 14:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0024_kidscoding_virtualclass"),
    ]

    operations = [
        migrations.AddField(
            model_name="course",
            name="kids_coding",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="coursecategory",
            name="child_1",
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AddField(
            model_name="coursecategory",
            name="child_2",
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]
