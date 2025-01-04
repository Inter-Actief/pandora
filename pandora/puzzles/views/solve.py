from django.urls import reverse
from django.views.generic import CreateView, ListView

from pandora.editions.mixins import CommitteeMemberAccessMixin, EditionMixin
from pandora.puzzles.forms.solve import SolveCreateForm
from pandora.puzzles.models import Solve
from pandora.teams.mixins import TeamAccessMixin


class SolveListView(EditionMixin, CommitteeMemberAccessMixin, ListView):
    model = Solve
    context_object_name = 'solves'

    def get_queryset(self):
        day = None if self.kwargs.get('day_number') is None else self.edition.days.filter(number=self.kwargs.get('day_number')).first()
        if not day:
            return Solve.objects.filter(code__day__isnull=True).order_by('-created_at')
        return Solve.objects.filter(code__day=day).order_by('-created_at')


class SolveCreateView(EditionMixin, TeamAccessMixin, CreateView):
    model = Solve
    form_class = SolveCreateForm
    template_name_suffix = '_create'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        kwargs['edition'] = self.edition
        return kwargs

    def get_initial(self):
        initial = super().get_initial()
        initial['puzzle_code'] = self.request.GET.get('code')
        return initial

    def get_success_url(self):
        return reverse('solve_add', kwargs={'year': self.edition.year})
