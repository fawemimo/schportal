# Generated by Django 4.1.4 on 2023-04-18 10:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0186_alter_student_cv_upload"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="billing",
            name="grand_outstanding",
        ),
        migrations.AlterField(
            model_name="billing",
            name="start_date",
            field=models.DateField(blank=True, null=True),
        ),
    ]