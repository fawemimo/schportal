# Generated by Django 4.1.4 on 2023-06-02 14:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0249_employer_industry'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='mainbanner',
            options={'ordering': ['-ordering']},
        ),
    ]
