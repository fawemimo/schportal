# Generated by Django 4.1.4 on 2023-02-02 08:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0033_merge_20230130_1144"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="mainbanner",
            name="ordering",
        ),
        migrations.AddField(
            model_name="course",
            name="course_outline_pdf",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="shortquiz",
            name="more_about_you",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="shortquiz",
            name="secondary_sch",
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name="shortquiz",
            name="secondary_studied",
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name="shortquiz",
            name="tartiary_education",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name="shortquiz",
            name="tartiary_studied",
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name="shortquiz",
            name="tech_interest",
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name="user",
            name="user_type",
            field=models.CharField(
                blank=True,
                choices=[("teacher", "Teacher"), ("student", "Student")],
                max_length=7,
                null=True,
            ),
        ),
    ]
