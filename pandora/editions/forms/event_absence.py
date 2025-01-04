from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db import transaction
from django.forms.models import ModelForm
from django.urls import reverse

from pandora.core.widgets import FormattedSelect
from pandora.editions.models import EventAbsence
from pandora.teams.models import Team


class EventAbsenceCreateForm(ModelForm):

    class Meta:
        model = EventAbsence
        fields = ('event', 'team_member', 'reason')
        widgets = {
            'event': FormattedSelect(format_label=lambda event: event.formatted_name)
        }

    team: Team

    def __init__(self, *args, **kwargs):
        self.team = kwargs.pop('team')
        super().__init__(*args, **kwargs)

        self.fields['event'].queryset = self.team.edition.events.filter(name__icontains='meeting')
        self.fields['team_member'].queryset = self.team.members

    @transaction.atomic
    def save(self, *args, **kwargs):
        instance = super().save(*args, **kwargs)

        # Send message to feed channels
        async_to_sync(get_channel_layer().group_send)(self.team.edition.get_feed_channel_group(), {
            'type': 'absence',
            'timestamp': instance.created_at.isoformat(),
            'message': f'{instance.team_member.name} ({instance.team_member.team.name}) requested absence for event {instance.event.name}.',
            'url': reverse('event_absences', kwargs={'year': self.team.edition.year, 'event_id': instance.event.id})
        })

        return instance


class EventAbsenceUpdateForm(ModelForm):
    class Meta:
        model = EventAbsence
        fields = ('status', 'feedback')
