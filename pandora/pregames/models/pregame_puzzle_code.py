from django.db import models
from django.db.models import Max
from django.urls import reverse

from pandora.core.models import BaseModel
from pandora.pregames.models.pregame import Pregame
from pandora.puzzles.models.puzzle import Puzzle
from pandora.teams.models.team import Team
from pandora.util import generate_random_string


def _generate_pregame_puzzle_code():
    return generate_random_string(10, digits=False)


class PregamePuzzleCode(BaseModel):

    class Meta:
        unique_together = ('pregame', 'code')

    number = models.PositiveSmallIntegerField()
    code = models.CharField(max_length=32, default=_generate_pregame_puzzle_code)

    pregame = models.ForeignKey(Pregame, related_name='puzzle_codes', on_delete=models.CASCADE)
    puzzle = models.OneToOneField(Puzzle, related_name='pregame_code', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.puzzle.name} - Pregame {self.pregame.edition.year} - {self.code}'

    @property
    def is_last(self):
        return self.number == self.pregame.puzzle_codes.aggregate(max_number=Max('number'))['max_number']

    def get_absolute_url(self):
        return reverse('puzzles', kwargs={'year': self.puzzle.edition.year})

    def get_update_url(self):
        return reverse('pregame_puzzle_code_update', kwargs={'year': self.puzzle.edition.year, 'puzzle_id': self.puzzle.id, 'pk': self.id})

    def get_delete_url(self):
        return reverse('pregame_puzzle_code_delete', kwargs={'year': self.puzzle.edition.year, 'puzzle_id': self.puzzle.id, 'pk': self.id})

    def get_found_for_team(self, team: Team):
        if self.number <= 1:
            return True
        return team.pregame_solves.filter(code__pregame=self.pregame, code__number=self.number - 1).exists()

    def get_solve_for_team(self, team: Team):
        return self.solves.filter(team=team).first()
