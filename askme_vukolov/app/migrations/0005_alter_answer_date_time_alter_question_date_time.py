# Generated by Django 4.1.2 on 2023-11-07 21:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_answer_is_correct'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='date_time',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='question',
            name='date_time',
            field=models.DateTimeField(),
        ),
    ]
