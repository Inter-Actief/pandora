from django.db import models
from django.urls import reverse

from pandora.core.models import BaseModel
from pandora.editions.models.committee_member import CommitteeMember
from pandora.puzzles.models.puzzle_code import PuzzleCode
from pandora.teams.models.team import Team


class Hint(BaseModel):

    class Status(models.TextChoices):
        WAITING = 'WAITING'
        IN_PROGRESS = 'IN_PROGRESS'
        FINISHED = 'FINISHED'
        CANCELED = 'CANCELED'

    class Meta:
        unique_together = ('code', 'team')

    status = models.CharField(max_length=32, choices=Status.choices, default=Status.WAITING)
    comment = models.TextField()
    phone_number = models.CharField(max_length=32, blank=True, null=True)
    committee_comment = models.TextField(blank=True)

    code = models.ForeignKey(PuzzleCode, related_name='hints', on_delete=models.CASCADE)
    team = models.ForeignKey(Team, related_name='hints', on_delete=models.CASCADE)
    committee_member = models.ForeignKey(CommitteeMember, related_name='hints', blank=True, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f'Hint - {self.team.name} - {self.code.puzzle.name}'

    @property
    def score(self):
        return -self.code.puzzle.edition.get_setting('puzzles.hint.score').as_int() if self.status != Hint.Status.CANCELED else 0

    def get_absolute_url(self):
        return reverse('hint', kwargs={'year': self.code.puzzle.edition.year, 'pk': self.id})

    def get_update_url(self):
        return reverse('hint_update', kwargs={'year': self.code.puzzle.edition.year, 'pk': self.id})

    def get_team_url(self):
        return reverse('hint_team', kwargs={'year': self.code.puzzle.edition.year, 'pk': self.id})

    def get_team_cancel_url(self):
        return reverse('hint_team_cancel', kwargs={'year': self.code.puzzle.edition.year, 'pk': self.id})
