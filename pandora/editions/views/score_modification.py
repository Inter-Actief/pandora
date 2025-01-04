from django.urls import reverse
from django.views.generic import CreateView, UpdateView, DeleteView

from pandora.editions.forms.score_modification import ScoreModificationCreateForm, ScoreModificationUpdateForm
from pandora.editions.mixins import CommitteeMemberAccessMixin, EditionMixin
from pandora.editions.models import ScoreModification


class ScoreModificationCreateView(EditionMixin, CommitteeMemberAccessMixin, CreateView):
    model = ScoreModification
    form_class = ScoreModificationCreateForm
    template_name_suffix = '_create'

    def get_initial(self):
        initial = super().get_initial()
        initial['team'] = self.kwargs.get('team_id')
        return initial


class ScoreModificationUpdateView(EditionMixin, CommitteeMemberAccessMixin, UpdateView):
    model = ScoreModification
    form_class = ScoreModificationUpdateForm
    template_name_suffix = '_update'
    context_object_name = 'score_modification'


class ScoreModificationDeleteView(EditionMixin, CommitteeMemberAccessMixin, DeleteView):
    model = ScoreModification
    template_name_suffix = '_delete'
    context_object_name = 'score_modification'

    def get_success_url(self):
        return self.object.team.get_absolute_url()
