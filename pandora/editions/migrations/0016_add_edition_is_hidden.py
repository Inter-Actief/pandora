# Generated by Django 4.1.7 on 2023-03-27 17:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('editions', '0015_add_event_is_hidden'),
    ]

    operations = [
        migrations.AddField(
            model_name='edition',
            name='is_hidden',
            field=models.BooleanField(default=False),
        ),
    ]
