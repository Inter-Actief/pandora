from django.views.generic import ListView

from pandora.editions.mixins import EditionMixin
from pandora.puzzles.models import PuzzleCode


class ParticipantPuzzleCodeListView(EditionMixin, ListView):
    model = PuzzleCode
    template_name = 'puzzles/participant_puzzlecode_list.html'
    context_object_name = 'puzzle_codes'
