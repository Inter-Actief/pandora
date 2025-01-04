from itertools import groupby

from django.urls import reverse
from django.views.generic import TemplateView

from pandora.editions.mixins import EditionMixin
from pandora.editions.models import Day
from pandora.teams.models import Team


def rank_teams(team_scores: list[tuple[int, Team]]):
    team_scores.sort(key=lambda pair: pair[0], reverse=True)
    return [(score, [pair[1] for pair in teams]) for score, teams in groupby(team_scores, key=lambda pair: pair[0])]


class ScoresDayView(EditionMixin, TemplateView):
    template_name = 'editions/scores_day.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        day = Day.objects.get(edition=self.edition, number=self.kwargs.get('day_number'))
        context['day'] = day

        team_scores = [(team.get_score(day), team) for team in self.edition.active_teams.all()]
        context['ranked_teams'] = rank_teams(team_scores)

        return context


class ScoresTotalView(EditionMixin, TemplateView):
    template_name = 'editions/scores_total.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        team_scores = [(team.total_score, team) for team in self.edition.active_teams.all()]
        context['ranked_teams'] = rank_teams(team_scores)

        return context


class ScoresModificationsView(EditionMixin, TemplateView):
    template_name = 'editions/scores_modifications.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        team_scores = [(team.total_bonus_score + team.total_offence_score, team) for team in self.edition.active_teams.all()]
        context['ranked_teams'] = rank_teams(team_scores)

        return context


class FeedView(EditionMixin, TemplateView):
    template_name = 'editions/feed.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['feed_websocket_url'] = self.request \
            .build_absolute_uri(reverse('edition_feed', urlconf='pandora.websocket_urls', kwargs={'edition_id': self.edition.id})) \
            .replace('http://', 'ws://') \
            .replace('https://', 'wss://')

        return context
