from typing import Optional, TYPE_CHECKING

from django.db import models
from django.urls import reverse

from pandora.core.models import BaseModel
from pandora.editions.models.edition import Edition

if TYPE_CHECKING:
    from pandora.puzzles.models.puzzle_code import PuzzleCode


class Day(BaseModel):

    class Meta:
        unique_together = ('edition', 'number')

    number = models.PositiveSmallIntegerField()
    start = models.DateTimeField()
    end = models.DateTimeField()

    edition = models.ForeignKey(Edition, related_name='days', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.edition.year} - Day {self.number}'

    @property
    def alive_teams(self):
        return [team for team in self.edition.active_teams.all() if self.kill_codes.filter(team_member__team=team, kill__isnull=True).exists()]

    @property
    def dead_teams(self):
        return [team for team in self.edition.active_teams.all() if not self.kill_codes.filter(team_member__team=team, kill__isnull=True).exists()]

    def get_puzzle_code(self, number: int) -> Optional['PuzzleCode']:
        return self.puzzle_codes.filter(number=number).first()

    def get_kill_code_export_url(self):
        return reverse('kill_code_export', kwargs={'year': self.edition.year, 'day_number': self.number})
