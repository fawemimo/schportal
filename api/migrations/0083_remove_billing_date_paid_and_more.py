# Generated by Django 4.1.4 on 2023-03-21 14:08

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0082_studentloansection"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="billing",
            name="date_paid",
        ),
        migrations.RemoveField(
            model_name="billing",
            name="outstanding_amount",
        ),
        migrations.AddField(
            model_name="billingdetail",
            name="outstanding_amount",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name="billingdetail",
            name="amount_paid",
            field=models.CharField(max_length=50),
        ),
        migrations.CreateModel(
            name="Payment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("transaction_ref", models.UUIDField(default=uuid.uuid4, unique=True)),
                ("first_name", models.CharField(max_length=255)),
                ("last_name", models.CharField(max_length=255)),
                ("email", models.EmailField(max_length=255)),
                ("phone_number", models.CharField(max_length=20)),
                ("total_amount", models.CharField(max_length=255)),
                ("paid_amount", models.CharField(max_length=255)),
                ("date_paid", models.DateField(auto_now_add=True)),
                (
                    "course",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="api.course"
                    ),
                ),
            ],
        ),
    ]
