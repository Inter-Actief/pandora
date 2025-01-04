from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from pandora.editions.mixins import EditionMixin
from pandora.teams.forms.participant_team import ParticipantTeamCreateForm, ParticipantTeamUpdateForm, ParticipantTeamPartialUpdateForm, \
    ParticipantTeamDeleteForm, ParticipantTeamJoinForm
from pandora.teams.mixins import TeamAccessMixin, LoginRequiredForJoinMixin
from pandora.teams.models import Team


class ParticipantTeamListView(EditionMixin, ListView):
    model = Team
    template_name = 'teams/participant_team_list.html'
    context_object_name = 'teams'

    def get_queryset(self):
        return self.edition.teams.order_by('status', 'name')


class ParticipantTeamCreateView(EditionMixin, LoginRequiredMixin, CreateView):
    model = Team
    form_class = ParticipantTeamCreateForm
    template_name = 'teams/participant_team_create.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        kwargs['edition'] = self.edition
        return kwargs

    def get_initial(self):
        initial = super().get_initial()
        initial['edition'] = str(self.edition.id)
        return initial

    def get_success_url(self):
        return self.object.get_participant_url()


class ParticipantTeamDetailView(EditionMixin, DetailView):
    model = Team
    template_name = 'teams/participant_team_detail.html'
    context_object_name = 'team'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['is_member'] = self.request.user.is_authenticated and self.object.members.filter(user=self.request.user).exists()
        context['is_edit_allowed'] = self.edition.get_setting('teams.edit.allowed').as_boolean()

        context['is_committee'] = self.request.user.is_authenticated and self.request.user.committee_memberships.filter(edition=self.object.edition).exists()

        context['day'] = self.object.edition.current_day

        return context


class ParticipantTeamUpdateView(EditionMixin, TeamAccessMixin, UpdateView):
    model = Team
    form_class = ParticipantTeamUpdateForm
    template_name = 'teams/participant_team_update.html'
    context_object_name = 'team'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['edition'] = self.edition
        return kwargs

    def get_team(self):
        return Team.objects.get(id=self.kwargs['pk'])

    def get_success_url(self):
        return self.object.get_participant_url()


class ParticipantTeamPartialUpdateView(EditionMixin, TeamAccessMixin, UpdateView):
    model = Team
    form_class = ParticipantTeamPartialUpdateForm
    template_name = 'teams/participant_team_update.html'
    context_object_name = 'team'

    def get_team(self):
        return Team.objects.get(id=self.kwargs['pk'])

    def get_success_url(self):
        return self.object.get_participant_url()


class ParticipantTeamDeleteView(EditionMixin, TeamAccessMixin, DeleteView):
    model = Team
    form_class = ParticipantTeamDeleteForm
    template_name = 'teams/participant_team_delete.html'
    context_object_name = 'team'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['edition'] = self.edition
        return kwargs

    def get_team(self):
        return Team.objects.get(id=self.kwargs['pk'])

    def get_success_url(self):
        return reverse('participant_edition', kwargs={'year': self.edition.year})


class ParticipantTeamJoinView(EditionMixin, LoginRequiredForJoinMixin, UpdateView):
    model = Team
    form_class = ParticipantTeamJoinForm
    template_name = 'teams/participant_team_join.html'
    context_object_name = 'team'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        kwargs['edition'] = self.edition
        return kwargs

    def get_initial(self):
        initial = super().get_initial()
        initial['join_code'] = self.kwargs.get('join_code')
        return initial

    def get_success_url(self):
        return self.object.get_participant_url()
