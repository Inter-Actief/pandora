from django.views.generic import ListView, DetailView

from pandora.editions.mixins import CommitteeMemberAccessMixin, EditionMixin
from pandora.teams.models import Team


class TeamListView(EditionMixin, CommitteeMemberAccessMixin, ListView):
    model = Team
    context_object_name = 'teams'

    def get_queryset(self):
        return self.edition.teams.order_by('status', 'name')


class TeamDetailView(EditionMixin, CommitteeMemberAccessMixin, DetailView):
    model = Team
    context_object_name = 'team'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['day'] = self.object.edition.current_day
        return context
