# Generated by Django 4.1.4 on 2023-04-19 10:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0202_rename_join_out_team_aboutussection_join_our_team_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="employer",
            old_name="posting_approval",
            new_name="profile_approval",
        ),
    ]