# Generated by Django 4.1.2 on 2023-11-09 13:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_ratetoanswer_ratetoquestion_delete_rate'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='cur_rate',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='ratetoanswer',
            name='parent',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rates', to='app.answer'),
        ),
        migrations.AlterField(
            model_name='ratetoquestion',
            name='parent',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rates', to='app.question'),
        ),
    ]