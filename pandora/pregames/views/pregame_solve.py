from django.views.generic import CreateView

from pandora.editions.mixins import EditionMixin
from pandora.pregames.forms.pregame_solve import PregameSolveCreateForm
from pandora.pregames.models import PregameSolve
from pandora.teams.mixins import TeamAccessMixin


class PregameSolveCreateView(EditionMixin, TeamAccessMixin, CreateView):
    model = PregameSolve
    form_class = PregameSolveCreateForm
    template_name_suffix = '_create'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        kwargs['edition'] = self.edition
        return kwargs
