from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse

from pandora.core.models import BaseModel
from pandora.editions.models.day import Day
from pandora.puzzles.models.puzzle import Puzzle
from pandora.teams.models.team import Team
from pandora.util import generate_random_string


def _generate_puzzle_code():
    return generate_random_string(10, digits=False)


class PuzzleCode(BaseModel):

    class Meta:
        unique_together = ('day', 'code')

    number = models.PositiveSmallIntegerField()
    code = models.CharField(max_length=32, default=_generate_puzzle_code)

    day = models.ForeignKey(Day, related_name='puzzle_codes', blank=True, null=True, on_delete=models.CASCADE,
                            help_text='Leaving the day blank makes it a bonus puzzle.')
    puzzle = models.OneToOneField(Puzzle, related_name='code', on_delete=models.CASCADE)

    def __str__(self):
        if self.day:
            return f'{self.puzzle.name} - Day {self.day.number} - {self.number}'
        return f'{self.puzzle.name} - Bonus - {self.number}'

    @property
    def is_bonus(self):
        return not self.day

    def clean(self):
        if self.day and self.day.edition != self.puzzle.edition:
            raise ValidationError('The day must be in the same edition as the puzzle.', code='invalid_day')

    def get_absolute_url(self):
        return reverse('puzzles', kwargs={'year': self.puzzle.edition.year})

    def get_update_url(self):
        return reverse('puzzle_code_update', kwargs={'year': self.puzzle.edition.year, 'puzzle_id': self.puzzle.id, 'pk': self.id})

    def get_delete_url(self):
        return reverse('puzzle_code_delete', kwargs={'year': self.puzzle.edition.year, 'puzzle_id': self.puzzle.id, 'pk': self.id})

    def get_found_for_team(self, team: Team):
        if self.number <= 1:
            return True
        return team.solves.filter(code__day=self.day, code__number=self.number - 1).exists()

    def get_solve_for_team(self, team: Team):
        return self.solves.filter(team=team).first()

    def get_hint_for_team(self, team: Team):
        from pandora.puzzles.models.hint import Hint

        return self.hints.filter(team=team).exclude(status=Hint.Status.CANCELED).first()
