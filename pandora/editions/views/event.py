from django.urls import reverse
from django.views.generic import DetailView, ListView

from pandora.editions.mixins import CommitteeMemberAccessMixin, EditionMixin
from pandora.editions.models import Event


class EventListView(EditionMixin, CommitteeMemberAccessMixin, ListView):
    model = Event
    context_object_name = 'events'

    def get_queryset(self):
        return self.edition.events.order_by('start')


class EventAttendanceView(EditionMixin, CommitteeMemberAccessMixin, DetailView):
    model = Event
    context_object_name = 'event'
    template_name_suffix = '_attendance'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['websocket_url'] = self.request\
            .build_absolute_uri(reverse('event_scanner', urlconf='pandora.websocket_urls', kwargs={'edition_id': self.edition.id, 'event_id': self.object.id}))\
            .replace('http://', 'ws://')\
            .replace('https://', 'wss://')

        return context


class EventScannerView(EditionMixin, CommitteeMemberAccessMixin, DetailView):
    model = Event
    context_object_name = 'event'
    template_name_suffix = '_scanner'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['websocket_url'] = self.request\
            .build_absolute_uri(reverse('event_scanner', urlconf='pandora.websocket_urls', kwargs={'edition_id': self.edition.id, 'event_id': self.object.id}))\
            .replace('http://', 'ws://')\
            .replace('https://', 'wss://')

        return context
