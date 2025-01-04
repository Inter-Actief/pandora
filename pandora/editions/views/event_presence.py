from django.views.generic import CreateView

from pandora.editions.forms.event_presence import EventPresenceCreateForm
from pandora.editions.mixins import CommitteeMemberAccessMixin, EditionMixin
from pandora.editions.models import EventPresence


class EventPresenceCreateView(EditionMixin, CommitteeMemberAccessMixin, CreateView):
    model = EventPresence
    form_class = EventPresenceCreateForm
    template_name_suffix = '_create'

    def get_initial(self):
        initial = super().get_initial()
        initial['event'] = self.kwargs.get('event_id')
        return initial
