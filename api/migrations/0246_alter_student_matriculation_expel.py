# Generated by Django 4.1.4 on 2023-05-24 13:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0245_alter_student_matriculation_graduation_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student_matriculation',
            name='expel',
            field=models.BooleanField(default=False, verbose_name='Expelled'),
        ),
    ]
