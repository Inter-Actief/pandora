# Generated by Django 4.1.5 on 2023-01-07 12:44

import pandora.puzzles.models.puzzle_code
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('puzzles', '0002_fix_solve_team'),
    ]

    operations = [
        migrations.AlterField(
            model_name='puzzlecode',
            name='code',
            field=models.CharField(default=pandora.puzzles.models.puzzle_code._generate_puzzle_code, max_length=32),
        ),
    ]
