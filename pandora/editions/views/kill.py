from django.urls import reverse
from django.views.generic import CreateView, ListView

from pandora.editions.forms.kill import KillCreateForm
from pandora.editions.mixins import CommitteeMemberAccessMixin, EditionMixin
from pandora.editions.models import Kill
from pandora.teams.mixins import TeamAccessMixin


class KillListView(EditionMixin, CommitteeMemberAccessMixin, ListView):
    model = Kill
    context_object_name = 'kills'

    def get_queryset(self):
        day = self.edition.days.filter(number=self.kwargs.get('day_number')).first()
        if not day:
            return Kill.objects.none()
        return Kill.objects.filter(code__day=day).order_by('-created_at')


class KillCreateView(EditionMixin, TeamAccessMixin, CreateView):
    model = Kill
    form_class = KillCreateForm
    template_name_suffix = '_create'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        kwargs['edition'] = self.edition
        return kwargs

    def get_initial(self):
        initial = super().get_initial()
        initial['kill_code'] = self.request.GET.get('code')
        return initial

    def get_success_url(self):
        return reverse('kill_add', kwargs={'year': self.edition.year})
