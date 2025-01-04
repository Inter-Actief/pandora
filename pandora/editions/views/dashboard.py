from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import TemplateView

from pandora.editions.mixins import CommitteeMemberAccessMixin, EditionMixin


class DashboardView(EditionMixin, LoginRequiredMixin, TemplateView):
    template_name = 'dashboards/user.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['team'] = self.edition.teams.filter(members__user=self.request.user).first()
        context['is_registration_allowed'] = self.edition.get_setting('teams.registration.allowed').as_boolean()

        return context


class CommitteeDashboardView(EditionMixin, CommitteeMemberAccessMixin, TemplateView):
    template_name = 'dashboards/committee.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['feed_url'] = reverse('committee_feed_dashboard', kwargs={'year': context['edition'].year})
        context['feed_websocket_url'] = self.request\
            .build_absolute_uri(reverse('edition_feed', urlconf='pandora.websocket_urls', kwargs={'edition_id': context['edition'].id}))\
            .replace('http://', 'ws://')\
            .replace('https://', 'wss://')

        return context


class CommitteeFeedDashboardView(EditionMixin, CommitteeMemberAccessMixin, TemplateView):
    template_name = 'dashboards/committee_feed.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['feed_websocket_url'] = self.request\
            .build_absolute_uri(reverse('edition_feed', urlconf='pandora.websocket_urls', kwargs={'edition_id': context['edition'].id}))\
            .replace('http://', 'ws://')\
            .replace('https://', 'wss://')

        return context
