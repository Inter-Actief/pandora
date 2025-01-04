from typing import Optional

from django import forms
from django.core.exceptions import ValidationError
from django.db import transaction
from django.forms import ModelForm
from django.http import HttpRequest

from pandora.editions.models import Edition, ScoreModification
from pandora.pregames.models import PregamePuzzleCode, PregameSolve
from pandora.teams.models import Team


class PregameSolveCreateForm(ModelForm):

    class Meta:
        model = PregameSolve
        fields = ()

    puzzle_code = forms.CharField(max_length=32)

    request: HttpRequest
    edition: Edition

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        self.edition = kwargs.pop('edition')
        super().__init__(*args, **kwargs)

    def _get_team(self) -> Optional[Team]:
        return self.edition.active_teams.filter(members__user=self.request.user).first()

    def _get_puzzle_code(self) -> Optional[PregamePuzzleCode]:
        return self.edition.pregame.puzzle_codes.filter(code=self.cleaned_data.get('puzzle_code')).first()

    def clean(self):
        if not self.edition.pregame or not self.edition.pregame.is_active:
            raise ValidationError('It is currently not a Pandora pregame.', code='no_pregame')

        team = self._get_team()
        if not team:
            raise ValidationError('You are not a member of a team.', code='no_team')

        puzzle_code = self._get_puzzle_code()
        if not puzzle_code:
            self.add_error('puzzle_code', '')
            raise ValidationError('Invalid pregame puzzle code.', code='invalid_puzzle_code')

        if PregameSolve.objects.filter(code=puzzle_code, team=team).exists():
            raise ValidationError('Your team already solved this pregame puzzle.', code='already_solved')

    @transaction.atomic
    def save(self, *args, **kwargs):
        self.instance.code = self._get_puzzle_code()
        self.instance.team = self._get_team()

        instance = super().save(*args, **kwargs)

        if instance.team.pregame_solves.filter(code__pregame=instance.code.pregame).count() == instance.code.pregame.puzzle_codes.count():
            score_modification = ScoreModification(
                type=ScoreModification.Type.BONUS,
                amount=instance.code.pregame.bonus_amount,
                reason=instance.code.pregame.bonus_reason,
                team=instance.team
            )
            score_modification.save()

        return instance
