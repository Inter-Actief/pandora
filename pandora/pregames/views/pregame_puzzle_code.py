from django.views.generic import CreateView, DeleteView, UpdateView

from pandora.editions.mixins import CommitteeMemberAccessMixin, EditionMixin
from pandora.pregames.forms.pregame_puzzle_code import PregamePuzzleCodeModelForm
from pandora.pregames.models import PregamePuzzleCode


class PregamePuzzleCodeCreateView(EditionMixin, CommitteeMemberAccessMixin, CreateView):
    model = PregamePuzzleCode
    form_class = PregamePuzzleCodeModelForm
    template_name_suffix = '_create'

    def get_initial(self):
        initial = super().get_initial()
        initial['pregame'] = self.edition.pregame
        initial['puzzle'] = self.kwargs.get('puzzle_id')
        return initial


class PregamePuzzleCodeUpdateView(EditionMixin, CommitteeMemberAccessMixin, UpdateView):
    model = PregamePuzzleCode
    form_class = PregamePuzzleCodeModelForm
    context_object_name = 'puzzle_code'
    template_name_suffix = '_update'


class PregamePuzzleCodeDeleteView(EditionMixin, CommitteeMemberAccessMixin, DeleteView):
    model = PregamePuzzleCode
    context_object_name = 'puzzle_code'
    template_name_suffix = '_delete'

    def get_success_url(self):
        return self.object.get_absolute_url()
