# Generated by Django 4.1.4 on 2023-05-25 11:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0246_alter_student_matriculation_expel'),
    ]

    operations = [
        migrations.AddField(
            model_name='billing',
            name='receipt_no',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]