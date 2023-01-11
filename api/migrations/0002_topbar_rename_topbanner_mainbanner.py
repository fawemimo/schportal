# Generated by Django 4.1.4 on 2022-12-26 13:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Topbar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150)),
                ('bar_src', models.TextField()),
            ],
        ),
        migrations.RenameModel(
            old_name='TopBanner',
            new_name='MainBanner',
        ),
    ]