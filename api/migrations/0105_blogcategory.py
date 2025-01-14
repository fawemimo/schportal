# Generated by Django 4.1.4 on 2023-03-30 14:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0104_alter_billingdetail_outstanding_amount"),
    ]

    operations = [
        migrations.CreateModel(
            name="BlogCategory",
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
                ("title", models.CharField(max_length=50)),
                ("slug", models.SlugField(blank=True, null=True)),
                ("seo_keywords", models.TextField()),
                ("date_created", models.DateTimeField(auto_now_add=True)),
                ("date_updated", models.DateTimeField(auto_now=True)),
            ],
            options={
                "ordering": ["-date_created"],
                "abstract": False,
            },
        ),
    ]
