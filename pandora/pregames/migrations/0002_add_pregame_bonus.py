# Generated by Django 4.1.7 on 2023-04-02 11:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pregames', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='pregame',
            name='bonus_amount',
            field=models.SmallIntegerField(default=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='pregame',
            name='bonus_reason',
            field=models.TextField(default='Solved pregame'),
            preserve_default=False,
        ),
    ]
