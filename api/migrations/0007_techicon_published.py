# Generated by Django 4.1.4 on 2022-12-29 22:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_navlink_remove_techicon_icon_img_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='techicon',
            name='published',
            field=models.BooleanField(default=False),
        ),
    ]