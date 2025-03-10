# Generated by Django 4.1.5 on 2023-01-05 21:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('editions', '0003_change_team_unique'),
    ]

    operations = [
        migrations.AddField(
            model_name='day',
            name='number',
            field=models.PositiveSmallIntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='day',
            unique_together={('edition', 'number')},
        ),
        migrations.AlterUniqueTogether(
            name='edition',
            unique_together={('year',)},
        ),
        migrations.RemoveField(
            model_name='day',
            name='type',
        ),
    ]
