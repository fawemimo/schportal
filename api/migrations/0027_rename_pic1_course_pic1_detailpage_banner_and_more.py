# Generated by Django 4.1.4 on 2023-01-22 16:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0026_alter_testimonial_batch'),
    ]

    operations = [
        migrations.RenameField(
            model_name='course',
            old_name='pic1',
            new_name='pic1_detailpage_banner',
        ),
        migrations.RenameField(
            model_name='course',
            old_name='pic2',
            new_name='pic2_detailpage_main',
        ),
    ]