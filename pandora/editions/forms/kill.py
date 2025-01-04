from typing import Optional

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django import forms
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.db import transaction
from django.forms import TextInput
from django.forms.models import ModelForm
from django.http import HttpRequest

from pandora.editions.models import Edition, KillCode, Kill
from pandora.teams.models import Team, TeamMember


class KillCreateForm(ModelForm):

    class Meta:
        model = Kill
        fields = ()

    kill_code = forms.CharField(max_length=32, widget=TextInput(attrs={'maxlength': 32, 'autocapitalize': 'none', 'autocomplete': 'off'}))

    request: HttpRequest
    edition: Edition

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        self.edition = kwargs.pop('edition')
        super().__init__(*args, **kwargs)

    def _get_team(self) -> Optional[Team]:
        return self.edition.active_teams.filter(members__user=self.request.user).first()

    def _get_team_member(self) -> Optional[TeamMember]:
        team = self._get_team()
        if not team:
            return None
        return team.members.filter(user=self.request.user).first()

    def _get_kill_code(self) -> Optional[KillCode]:
        return self.edition.current_day.kill_codes.filter(code=self.cleaned_data.get('kill_code')).first()

    def clean(self):
        if not self.edition.current_day:
            raise ValidationError('It is currently not a Pandora day.', code='no_day')

        team = self._get_team()
        if not team:
            raise ValidationError('You are not a member of a team.', code='no_team')

        kill_code = self._get_kill_code()
        if not kill_code:
            self.add_error('kill_code', '')
            raise ValidationError('Invalid kill code.', code='invalid_kill_code')

        team_member = self._get_team_member()
        if kill_code.team_member == team_member:
            raise ValidationError('You are not allowed to commit suicide.', code='suicide')

        if kill_code.team_member.team == team:
            raise ValidationError('You are not allowed to kill your team members.', code='friendly_fire')

        if Kill.objects.filter(code=kill_code).exists():
            raise ValidationError('This kill code has already been entered.', code='already_killed')

    @transaction.atomic
    def save(self, *args, **kwargs):
        self.instance.code = self._get_kill_code()
        self.instance.killer = self._get_team_member()

        instance = super().save(*args, **kwargs)

        day = instance.code.day
        killer = instance.killer
        victim = instance.victim

        # Add message
        messages.success(self.request, f'You killed {victim.name} from team {victim.team.name}.')

        # Send message to feed channels
        async_to_sync(get_channel_layer().group_send)(self.edition.get_feed_channel_group(), {
            'type': 'kill',
            'timestamp': instance.created_at.isoformat(),
            'message': f'{killer.name} ({killer.team.name}) killed {victim.name} ({victim.team.name}).',
            'kill': {
                'killer': {
                    'id': str(killer.id),
                    'name': killer.name,
                    'team': {
                        'id': str(killer.team.id),
                        'name': killer.team.name
                    }
                },
                'victim': {
                    'id': str(victim.id),
                    'name': victim.name,
                    'team': {
                        'id': str(victim.team.id),
                        'name': victim.team.name
                    }
                }
            },
            'day': {
                'id': str(day.id),
                'number': day.number
            }
        })

        if victim.team.get_is_eliminated(day):
            # Send message to feed channels
            async_to_sync(get_channel_layer().group_send)(self.edition.get_feed_channel_group(), {
                'type': 'elimination',
                'timestamp': instance.created_at.isoformat(),
                'message': f'{victim.team.name} has been eliminated from day {day.number}.',
                'team': {
                    'id': str(victim.team.id),
                    'name': victim.team.name
                },
                'day': {
                    'id': str(day.id),
                    'number': day.number
                }
            })

        return instance
