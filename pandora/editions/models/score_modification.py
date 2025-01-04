from django.db import models
from django.urls import reverse

from pandora.core.models import BaseModel
from pandora.teams.models.team import Team
from pandora.teams.models.team_member import TeamMember


class ScoreModification(BaseModel):

    class Type(models.TextChoices):
        BONUS = 'BONUS', 'Bonus'
        OFFENCE = 'OFFENCE', 'Offence'

    type = models.CharField(max_length=32, choices=Type.choices)
    amount = models.SmallIntegerField(help_text='Amounts are absolute, so bonus is positive, offence is negative.')
    reason = models.TextField()

    team = models.ForeignKey(Team, related_name='score_modifications', on_delete=models.CASCADE)
    team_member = models.ForeignKey(TeamMember, related_name='score_modifications', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f'{self.team.name} - {self.get_type_display()} - {self.amount} points'

    def get_absolute_url(self):
        return self.team.get_absolute_url()

    def get_update_url(self):
        return reverse('score_modification_update', kwargs={'year': self.team.edition.year, 'team_id': self.team.id, 'pk': self.id})

    def get_delete_url(self):
        return reverse('score_modification_delete', kwargs={'year': self.team.edition.year, 'team_id': self.team.id, 'pk': self.id})
