# Generated by Django 5.1.5 on 2025-02-01 12:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quizmania', '0020_remove_quizsession_last_question_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='quizsession',
            name='current_question',
        ),
        migrations.AddField(
            model_name='quizsession',
            name='current_question_id',
            field=models.IntegerField(blank=True, default=None, null=True),
        ),
    ]
