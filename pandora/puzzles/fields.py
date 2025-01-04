from django.forms import ModelChoiceField

from pandora.puzzles.models import PuzzleCode
from pandora.teams.models import Team


class PuzzleCodeChoiceField(ModelChoiceField):

    team: Team = None

    def label_from_instance(self, obj: PuzzleCode):
        puzzle_name = obj.puzzle.name if self.team and obj.get_found_for_team(self.team) else '?'
        return f'Day {obj.day.number} - Puzzle {obj.number} - {puzzle_name}'
