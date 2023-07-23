# Generated by Django 4.1.4 on 2023-07-22 22:54

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0254_question_topic_questioncomment_question_topics'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='batch',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.batch'),
        ),
        migrations.AlterField(
            model_name='question',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.student'),
        ),
    ]
