from django.core.exceptions import ValidationError
from django.db import models

from pandora.core.models import BaseModel
from pandora.editions.models.day import Day
from pandora.teams.models.team import Team


class ArchiveScore(BaseModel):

    class Type(models.TextChoices):
        DAY = 'DAY', 'Day'
        BONUS = 'BONUS', 'Bonus'
        OFFENCE = 'OFFENCE', 'Offence'
        OTHER = 'OTHER', 'Other'
        TOTAL = 'TOTAL', 'Total'

    class Meta:
        unique_together = ('type', 'day', 'team')

    type = models.CharField(max_length=32, choices=Type.choices)
    score = models.SmallIntegerField(help_text='Amounts are absolute, so bonus is positive, offence is negative.')

    day = models.ForeignKey(Day, related_name='archive_scores', blank=True, null=True, on_delete=models.CASCADE,
                            help_text='Leaving the day blank makes it a bonus puzzle.')
    team = models.ForeignKey(Team, related_name='archive_scores', on_delete=models.CASCADE)

    def __str__(self):
        if self.day:
            return f'{self.team.edition.year} - {self.get_type_display()} {self.day.number} - {self.team.name}'
        return f'{self.team.edition.year} - {self.get_type_display()} - {self.team.name}'

    def clean(self):
        if self.type == ArchiveScore.Type.DAY and not self.day:
            raise ValidationError('Type can\'t be day unless the score is linked to a day.')
        elif self.type != ArchiveScore.Type.DAY and self.day:
            raise ValidationError('Type can only be day if the score is linked to a day.')

        if self.day and self.day.edition != self.team.edition:
            raise ValidationError('The day must be in the same edition as the team.', code='invalid_day')
