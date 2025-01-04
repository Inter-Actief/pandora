from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView

from pandora.editions.mixins import CommitteeMemberAccessMixin, EditionMixin
from pandora.puzzles.forms.puzzle import PuzzleModelForm
from pandora.puzzles.models import Puzzle


class PuzzleListView(EditionMixin, CommitteeMemberAccessMixin, ListView):
    model = Puzzle
    context_object_name = 'puzzles'

    def get_queryset(self):
        return self.edition.puzzles.order_by('name')


class PuzzleCreateView(EditionMixin, CommitteeMemberAccessMixin, CreateView):
    model = Puzzle
    form_class = PuzzleModelForm
    template_name_suffix = '_create'

    def get_initial(self):
        initial = super().get_initial()
        initial['edition'] = str(self.edition.id)
        initial['solution_direction'] = Puzzle.Direction.NONE
        return initial


class PuzzleDetailView(EditionMixin, CommitteeMemberAccessMixin, DetailView):
    model = Puzzle
    context_object_name = 'puzzle'


class PuzzleUpdateView(EditionMixin, CommitteeMemberAccessMixin, UpdateView):
    model = Puzzle
    form_class = PuzzleModelForm
    context_object_name = 'puzzle'
    template_name_suffix = '_update'


class PuzzleDeleteView(EditionMixin, CommitteeMemberAccessMixin, DeleteView):
    model = Puzzle
    context_object_name = 'puzzle'
    template_name_suffix = '_delete'

    def get_success_url(self):
        return self.edition.get_puzzles_url()
