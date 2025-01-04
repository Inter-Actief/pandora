from django.db import models
from django.urls import reverse

from pandora.core.models import BaseModel
from pandora.pregames.models.pregame_puzzle_code import PregamePuzzleCode
from pandora.teams.models.team import Team


class PregameSolve(BaseModel):

    class Meta:
        unique_together = ('code', 'team')

    code = models.ForeignKey(PregamePuzzleCode, related_name='solves', on_delete=models.CASCADE)
    team = models.ForeignKey(Team, related_name='pregame_solves', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.team.name} solved {self.puzzle.name} ({self.code.code})'

    @property
    def puzzle(self):
        return self.code.puzzle

    def get_absolute_url(self):
        return reverse('pregame_solve_add', kwargs={'year': self.puzzle.edition.year})