# Generated by Django 4.1.4 on 2023-05-18 14:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0238_remove_student_student_idcard_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Student_Matriculation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('matric_number', models.CharField(max_length=50, unique=True)),
                ('expel', models.BooleanField(default=False)),
                ('job_ready', models.BooleanField(default=False, help_text='to control student for job applications')),
                ('matric_date', models.DateField()),
                ('graduation_date', models.DateField()),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('residential_address', models.CharField(max_length=250)),
                ('contact_address', models.CharField(max_length=250)),
                ('next_of_kin_fullname', models.CharField(max_length=150)),
                ('next_of_kin_contact_address', models.CharField(max_length=250)),
                ('next_of_kin_mobile_number', models.CharField(max_length=250)),
                ('relationship_with_next_kin', models.CharField(max_length=255)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='api.student')),
            ],
        ),
    ]
