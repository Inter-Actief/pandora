from django.db import models

from pandora.core.models import BaseModel
from pandora.puzzles.models.puzzle_code import PuzzleCode
from pandora.teams.models.team import Team


class Solve(BaseModel):

    class Meta:
        unique_together = ('code', 'team')

    code = models.ForeignKey(PuzzleCode, related_name='solves', on_delete=models.CASCADE)
    team = models.ForeignKey(Team, related_name='solves', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.team.name} solved {self.puzzle.name} ({self.code.code})'

    @property
    def puzzle(self):
        return self.code.puzzle

    @property
    def score(self):
        scores = self.code.puzzle.edition.get_setting('puzzles.score').as_int_list()

        return scores[min(self.code.number - 1, len(scores) - 1)] if self.code.day_id else scores[0]

    @property
    def score_with_hint(self):
        score = self.score

        hint = self.code.get_hint_for_team(self.team)
        if hint:
            score -= self.code.puzzle.edition.get_setting('puzzles.hint.score').as_int()

        return score
