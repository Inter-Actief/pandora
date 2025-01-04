from typing import Any

from django.contrib import messages
from django.contrib.auth.mixins import AccessMixin, LoginRequiredMixin
from django.http import HttpRequest

from pandora.editions.models import Edition
from pandora.teams.models import Team


class LoginRequiredForJoinMixin(LoginRequiredMixin):

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.info(request, 'Please sign in to join this team.')

        return super().dispatch(request, *args, **kwargs)


class TeamAccessMixin(AccessMixin):

    request: HttpRequest
    edition: Edition
    kwargs: dict[str, Any]

    def get_team(self):
        if 'team_id' in self.kwargs:
            return Team.objects.get(id=self.kwargs.get('team_id'))

        return Team.objects.get(edition=self.edition, members__user=self.request.user)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()

        team = self.get_team()
        if not team.members.filter(user=request.user).exists():
            return self.handle_no_permission()

        return super().dispatch(request, *args, **kwargs)
