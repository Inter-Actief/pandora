from django.contrib import messages
from django.shortcuts import redirect
from django.views.generic.edit import UpdateView, DeleteView

from pandora.editions.mixins import EditionMixin
from pandora.teams.forms.participant_team_member import TeamMemberUpdateForm, TeamMemberDeleteForm
from pandora.teams.mixins import TeamAccessMixin
from pandora.teams.models import TeamMember


class TeamMemberParticipantUpdateView(EditionMixin, TeamAccessMixin, UpdateView):
    model = TeamMember
    form_class = TeamMemberUpdateForm
    template_name = 'teams/participant_teammember_update.html'
    context_object_name = 'member'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['edition'] = self.edition
        return kwargs


class TeamMemberParticipantDeleteView(EditionMixin, TeamAccessMixin, DeleteView):
    model = TeamMember
    form_class = TeamMemberDeleteForm
    template_name = 'teams/participant_teammember_delete.html'
    context_object_name = 'member'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['edition'] = self.edition
        return kwargs

    def get_success_url(self):
        return self.object.team.get_participant_url()

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)

        if self.object.team.members.count() == 1:
            messages.error(request, 'You are the only member left in the team, so you can\'t be removed. Please disband the team instead.')
            return redirect(self.object.team.get_participant_url())

        if self.object.user == request.user:
            messages.warning(request, 'You are about to remove yourself from the team.')

        return response
