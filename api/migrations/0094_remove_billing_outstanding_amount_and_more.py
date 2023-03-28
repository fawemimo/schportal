# Generated by Django 4.1.4 on 2023-03-28 02:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0093_alter_billingdetail_amount_paid"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="billing",
            name="outstanding_amount",
        ),
        migrations.AddField(
            model_name="billingdetail",
            name="outstanding_amount",
            field=models.PositiveBigIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="billingdetail",
            name="program_type",
            field=models.CharField(
                blank=True,
                choices=[("Onsite", "Onsite"), ("Virtual", "Virtual")],
                max_length=50,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="billing",
            name="total_amount",
            field=models.PositiveBigIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="billing",
            name="total_amount_paid",
            field=models.PositiveBigIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="billingdetail",
            name="amount_paid",
            field=models.PositiveBigIntegerField(),
        ),
    ]