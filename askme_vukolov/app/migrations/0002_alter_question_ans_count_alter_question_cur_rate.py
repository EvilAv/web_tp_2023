# Generated by Django 4.1.2 on 2023-11-07 17:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='ans_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='question',
            name='cur_rate',
            field=models.IntegerField(default=0),
        ),
    ]
