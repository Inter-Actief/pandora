from typing import Optional

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django import forms
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.db import transaction
from django.forms import ModelForm, TextInput
from django.http import HttpRequest

from pandora.editions.models import Edition
from pandora.puzzles.models import PuzzleCode, Solve, Hint
from pandora.teams.models import Team


class SolveCreateForm(ModelForm):
    class Meta:
        model = Solve
        fields = ()

    puzzle_code = forms.CharField(max_length=32, widget=TextInput(attrs={'maxlength': 32, 'autocapitalize': 'none', 'autocomplete': 'off'}))

    request: HttpRequest
    edition: Edition

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        self.edition = kwargs.pop('edition')
        super().__init__(*args, **kwargs)

    def _get_team(self) -> Optional[Team]:
        return self.edition.active_teams.filter(members__user=self.request.user).first()

    def _get_puzzle_code(self) -> Optional[PuzzleCode]:
        return PuzzleCode.objects.filter(puzzle__edition=self.edition).filter(code=self.cleaned_data.get('puzzle_code')).first()

    def clean(self):
        if not self.edition.current_day:
            raise ValidationError('It is currently not a Pandora day.', code='no_day')

        team = self._get_team()
        if not team:
            raise ValidationError('You are not a member of a team.', code='no_team')

        puzzle_code = self._get_puzzle_code()
        if not puzzle_code:
            self.add_error('puzzle_code', '')
            raise ValidationError('Invalid puzzle code.', code='invalid_puzzle_code')

        if Solve.objects.filter(code=puzzle_code, team=team).exists():
            raise ValidationError('Your team already solved this puzzle.', code='already_solved')

    @transaction.atomic
    def save(self, *args, **kwargs):
        self.instance.code = self._get_puzzle_code()
        self.instance.team = self._get_team()

        instance = super().save(*args, **kwargs)

        # Mark the hint as finished
        hint = instance.code.get_hint_for_team(instance.team)
        if hint:
            hint.status = Hint.Status.FINISHED
            hint.save()

        day = instance.code.day
        message_puzzle = f'puzzle {instance.code.number} of day {day.number}' if day else f'bonus puzzle {instance.code.number}'

        # Add message
        messages.success(self.request, f'Your team solved {message_puzzle}.')

        # Send message to feed channels
        async_to_sync(get_channel_layer().group_send)(self.edition.get_feed_channel_group(), {
            'type': 'solve',
            'timestamp': instance.created_at.isoformat(),
            'message': f'{instance.team.name} solved {message_puzzle}.',
            'solve': {
                'team': {
                    'id': str(instance.team.id),
                    'name': instance.team.name
                },
                'code': {
                    'day': {
                        'number': day.number
                    } if day else None,
                    'number': instance.code.number,
                }
            }
        })

        if day and instance.team.solves.filter(code__day=day).count() == day.puzzle_codes.count():
            # Send message to feed channels
            async_to_sync(get_channel_layer().group_send)(self.edition.get_feed_channel_group(), {
                'type': 'completion',
                'timestamp': instance.created_at.isoformat(),
                'message': f'{instance.team.name} solved all day {day.number} puzzles.',
                'team': {
                    'id': str(instance.team.id),
                    'name': instance.team.name
                },
                'day': {
                    'id': str(day.id),
                    'number': day.number
                }
            })

        return instance
