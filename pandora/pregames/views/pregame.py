from django.db.models import Max, Count
from django.views.generic import TemplateView

from pandora.editions.mixins import EditionMixin


class PregameScoresView(EditionMixin, TemplateView):
    template_name = 'pregames/scores.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['pregame'] = self.edition.pregame
        context['teams'] = self.edition.active_teams\
            .annotate(pregame_solve_count=Count('pregame_solves'), pregame_last_solved_at=Max('pregame_solves__created_at'))\
            .order_by('-pregame_solve_count', 'pregame_last_solved_at')\
            .all()

        return context
