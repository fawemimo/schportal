# Generated by Django 4.1.4 on 2023-03-29 12:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0103_rename_intro_txt_internationalmodel_why_choose_virtual"),
    ]

    operations = [
        migrations.AlterField(
            model_name="billingdetail",
            name="outstanding_amount",
            field=models.PositiveBigIntegerField(blank=True, editable=False, null=True),
        ),
    ]