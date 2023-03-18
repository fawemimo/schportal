# Generated by Django 4.1.4 on 2023-03-15 13:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0064_aboutussection"),
    ]

    operations = [
        migrations.AddField(
            model_name="sponsorship",
            name="organisation_name",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name="financialaid",
            name="aid_type",
            field=models.CharField(
                choices=[
                    ("Student Loan", "Student Loan"),
                    (
                        "Full Scholarship(Tuition + Laptop + Stipend)",
                        "Full Scholarship(Tuition + Laptop + Stipend)",
                    ),
                    (
                        "Scholarship Tier 1 (Tuition + Laptop)",
                        "Scholarship Tier 1 (Tuition + Laptop)",
                    ),
                    ("Scholarship Tier 2 (Tuition)", "Scholarship Tier 2 (Tuition)"),
                ],
                max_length=50,
            ),
        ),
    ]