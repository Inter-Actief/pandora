from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView, ListView

from pandora.editions.mixins import CommitteeMemberAccessMixin, EditionMixin
from pandora.puzzles.forms.hint import HintCreateForm, HintCancelForm, HintUpdateForm
from pandora.puzzles.models import Hint
from pandora.teams.mixins import TeamAccessMixin


class HintCreateView(EditionMixin, TeamAccessMixin, CreateView):
    model = Hint
    form_class = HintCreateForm
    template_name_suffix = '_create'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        kwargs['edition'] = self.edition
        return kwargs

    def get_success_url(self):
        return self.object.get_team_url()


class HintListView(EditionMixin, CommitteeMemberAccessMixin, ListView):
    model = Hint
    context_object_name = 'hints'

    def get_queryset(self):
        return Hint.objects.filter(code__puzzle__edition=self.edition).order_by('-created_at')


class HintDetailView(EditionMixin, CommitteeMemberAccessMixin, DetailView):
    model = Hint
    context_object_name = 'hint'


class HintUpdateView(EditionMixin, CommitteeMemberAccessMixin, UpdateView):
    model = Hint
    form_class = HintUpdateForm
    template_name_suffix = '_update'
    context_object_name = 'hint'


class HintTeamDetailView(EditionMixin, TeamAccessMixin, DetailView):
    model = Hint
    template_name_suffix = '_team_detail'
    context_object_name = 'hint'

    def get_team(self):
        return self.get_object().team


class HintTeamCancelView(EditionMixin, TeamAccessMixin, UpdateView):
    model = Hint
    form_class = HintCancelForm
    template_name_suffix = '_team_cancel'
    context_object_name = 'hint'

    def get_team(self):
        return self.get_object().team

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['edition'] = self.edition
        return kwargs

    def get_initial(self):
        initial = super().get_initial()
        initial['status'] = Hint.Status.CANCELED
        return initial
