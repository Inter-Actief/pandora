from django.forms import HiddenInput
from django.forms.models import ModelForm

from pandora.core.widgets import SearchableSelect
from pandora.editions.models import Event, EventPresence


class EventPresenceCreateForm(ModelForm):

    class Meta:
        model = EventPresence
        fields = ('event', 'team_member')
        widgets = {
            'event': HiddenInput(),
            'team_member': SearchableSelect(attrs={'autofocus': True}, format_label=lambda team_member: team_member.user.get_full_name())
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['team_member'].queryset = Event.objects.get(id=self.initial['event']).missing_team_members.prefetch_related('user')
