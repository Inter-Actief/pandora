# Generated by Django 4.1.7 on 2023-04-02 11:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0008_change_team_member_code'),
        ('editions', '0017_add_committee_member_is_hidden'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scoremodification',
            name='team_member',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='score_modifications', to='teams.teammember'),
        ),
    ]
