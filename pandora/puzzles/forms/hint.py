from typing import Optional

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.core.exceptions import ValidationError
from django.db import transaction
from django.forms import ModelForm, HiddenInput
from django.http import HttpRequest
from django.urls import reverse

from pandora.editions.models import Edition
from pandora.puzzles.fields import PuzzleCodeChoiceField
from pandora.puzzles.models import PuzzleCode, Hint
from pandora.teams.models import Team


class HintCreateForm(ModelForm):

    class Meta:
        model = Hint
        fields = ('code', 'comment', 'phone_number')

    request: HttpRequest
    edition: Edition

    code = PuzzleCodeChoiceField(queryset=None)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        self.edition = kwargs.pop('edition')
        super().__init__(*args, **kwargs)

        if self.edition.current_day:
            self.fields['code'].queryset = self.edition.current_day.puzzle_codes.order_by('number')
            self.fields['code'].team = self._get_team()
        else:
            self.fields['code'].queryset = PuzzleCode.objects.none()

    def _get_team(self) -> Optional[Team]:
        return self.edition.active_teams.filter(members__user=self.request.user).first()

    def clean(self):
        if not self.edition.current_day:
            raise ValidationError('It is currently not a Pandora day.', code='no_day')

        team = self._get_team()
        if not team:
            raise ValidationError('You are not a member of a team.', code='no_team')

        if Hint.objects.filter(code=self.cleaned_data.get('code'), team=team).exclude(status=Hint.Status.CANCELED).exists():
            raise ValidationError('Your team already requested a hint for this puzzle.', code='already_requested')

    @transaction.atomic
    def save(self, *args, **kwargs):
        self.instance.team = self._get_team()

        instance = super().save(*args, **kwargs)

        day = instance.code.day
        message_puzzle = f'puzzle {instance.code.number} of day {day.number}' if day else f'bonus puzzle {instance.code.number}'

        # Send message to feed channels
        async_to_sync(get_channel_layer().group_send)(self.edition.get_feed_channel_group(), {
            'type': 'hint',
            'timestamp': instance.created_at.isoformat(),
            'message': f'{instance.team.name} requested a hint for {message_puzzle}.',
            'url': reverse('hint', kwargs={'year': self.edition.year, 'pk': instance.id})
        })

        return instance


class HintUpdateForm(ModelForm):

    class Meta:
        model = Hint
        fields = ('status', 'committee_member', 'committee_comment')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['committee_member'].queryset = self.instance.code.puzzle.edition.committee_members


class HintCancelForm(ModelForm):

    class Meta:
        model = Hint
        fields = ('status', )
        widgets = {
            'status': HiddenInput()
        }

    edition: Edition

    def __init__(self, *args, **kwargs):
        self.edition = kwargs.pop('edition')
        super().__init__(*args, **kwargs)

    def clean(self):
        if not self.edition.current_day:
            raise ValidationError('It is currently not a Pandora day.', code='no_day')

        if self.cleaned_data.get('status') != Hint.Status.CANCELED:
            raise ValidationError('Hint status must be canceled.', code='invalid_status')

        if self.instance.status != Hint.Status.WAITING:
            raise ValidationError('Hint cannot be canceled, because it is already in progress, finished or canceled.', code='not_waiting')
