# Generated by Django 4.1.2 on 2023-11-09 00:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_alter_answer_date_time_alter_question_date_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='tag',
            name='uses',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='question',
            name='ans_count',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
