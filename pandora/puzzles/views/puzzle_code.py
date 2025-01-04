from django.views.generic import CreateView, DeleteView, UpdateView

from pandora.editions.mixins import CommitteeMemberAccessMixin, EditionMixin
from pandora.puzzles.forms.puzzle_code import PuzzleCodeModelForm
from pandora.puzzles.models import PuzzleCode


class PuzzleCodeCreateView(EditionMixin, CommitteeMemberAccessMixin, CreateView):
    model = PuzzleCode
    form_class = PuzzleCodeModelForm
    template_name_suffix = '_create'

    def get_initial(self):
        initial = super().get_initial()
        initial['puzzle'] = self.kwargs.get('puzzle_id')
        return initial


class PuzzleCodeUpdateView(EditionMixin, CommitteeMemberAccessMixin, UpdateView):
    model = PuzzleCode
    form_class = PuzzleCodeModelForm
    context_object_name = 'puzzle_code'
    template_name_suffix = '_update'


class PuzzleCodeDeleteView(EditionMixin, CommitteeMemberAccessMixin, DeleteView):
    model = PuzzleCode
    context_object_name = 'puzzle_code'
    template_name_suffix = '_delete'

    def get_success_url(self):
        return self.object.get_absolute_url()
