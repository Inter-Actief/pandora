from asgiref.sync import async_to_sync
from channels.generic.websocket import JsonWebsocketConsumer
from django.db import transaction

from pandora.editions.models import Event, EventPresence, EventAbsence
from pandora.teams.models import TeamMember, Team


class EventScannerConsumer(JsonWebsocketConsumer):

    def _get_event(self):
        return Event.objects.get(id=self.scope['url_route']['kwargs']['event_id'])

    def connect(self):
        event = self._get_event()

        user = self.scope['user']

        if not user.is_authenticated:
            raise PermissionError('User must be authenticated.')
        if not event.edition.committee_members.filter(user=user).exists():
            raise PermissionError('User must be a committee member of the current Pandora edition.')

        async_to_sync(self.channel_layer.group_add)(event.get_scanner_channel_group(), self.channel_name)
        super().connect()

    def disconnect(self, code):
        event = self._get_event()
        async_to_sync(self.channel_layer.group_discard)(event.get_scanner_channel_group(), self.channel_name)
        super().disconnect(code)

    @transaction.atomic
    def receive_json(self, content, **kwargs):
        event = self._get_event()

        code = content.get('code', '')
        data = {
            'code': code
        }

        # Find team member
        member = TeamMember.objects.filter(team__edition=event.edition).filter(code=code).first()
        if not member:
            self.send_json({
                'status': 'no_member',
                'message': 'Invalid team member code.',
                **data
            })
            return

        data = {
            **data,
            'name': member.user.get_full_name(),
            'member': {
                'id': str(member.id),
                'name': member.name
            },
            'team': {
                'id': str(member.team.id),
                'name': member.team.name
            }
        }

        if member.team.status != Team.Status.ACTIVE:
            self.send_json({
                'status': 'inactive_team',
                'message': 'Team is not active.',
                **data
            })
            return

        # Check member presence
        if EventPresence.objects.filter(event=event, team_member=member).count() > 0:
            self.send_json({
                'status': 'already_present',
                'message': 'Team member is already present at this event.',
                **data
            })
            return

        # Check member absence
        if EventAbsence.objects.filter(event=event, team_member=member).count() > 0:
            self.send_json({
                'status': 'already_absent',
                'message': 'Team member is already absent from this event.',
                **data
            })
            return

        # Store member presence
        presence = EventPresence(event=event, team_member=member)
        presence.save()

        # Send team and team member details to all connected channels
        async_to_sync(self.channel_layer.group_send)(event.get_scanner_channel_group(), {
            'type': 'event.member',
            'status': 'present',
            **data
        })

    def event_member(self, message):
        # Send received group message to channel
        self.send_json(message)
