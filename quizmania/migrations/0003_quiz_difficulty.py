# Generated by Django 5.1.5 on 2025-01-22 10:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quizmania', '0002_rename_question_answer_question'),
    ]

    operations = [
        migrations.AddField(
            model_name='quiz',
            name='difficulty',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='quizes', to='quizmania.difficulty'),
        ),
    ]
