# Generated by Django 4.1.4 on 2023-04-12 13:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0146_rename_grand_outstanding_billing_total_amount_paid_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="billing",
            name="course",
        ),
        migrations.AddField(
            model_name="billing",
            name="schedule",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="api.schedule",
            ),
        ),
        migrations.AddField(
            model_name="billingdetail",
            name="course_fee",
            field=models.PositiveBigIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="extraitem",
            name="item_name_fee",
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
