from django.urls import reverse
from django.views.generic import CreateView, ListView, UpdateView

from pandora.editions.forms.event_absence import EventAbsenceCreateForm, EventAbsenceUpdateForm
from pandora.editions.mixins import EditionMixin, CommitteeMemberAccessMixin
from pandora.editions.models import EventAbsence
from pandora.teams.mixins import TeamAccessMixin


class EventAbsenceListView(EditionMixin, CommitteeMemberAccessMixin, ListView):
    model = EventAbsence
    context_object_name = 'absences'

    def get_queryset(self):
        event = self.edition.events.get(id=self.kwargs.get('event_id'))
        return event.absences.order_by('-created_at')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['event'] = self.edition.events.get(id=self.kwargs.get('event_id'))
        return context_data


class EventAbsenceCreateView(EditionMixin, TeamAccessMixin, CreateView):
    model = EventAbsence
    form_class = EventAbsenceCreateForm
    template_name = 'editions/participant_eventabsence_create.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['team'] = self.get_team()
        return kwargs

    def get_success_url(self):
        return reverse('dashboard', kwargs={'year': self.edition.year})


class EventAbsenceUpdateView(EditionMixin, CommitteeMemberAccessMixin, UpdateView):
    model = EventAbsence
    form_class = EventAbsenceUpdateForm
    template_name_suffix = '_update'
    context_object_name = 'absence'
