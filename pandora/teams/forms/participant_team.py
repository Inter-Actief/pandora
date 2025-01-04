from django import forms
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.db import transaction
from django.forms import HiddenInput, Form
from django.forms.models import ModelForm

from pandora.teams.models import Team, TeamMember


class ParticipantTeamCreateForm(ModelForm):
    class Meta:
        model = Team
        fields = ('edition', 'name')
        widgets = {
            'edition': HiddenInput()
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        self.edition = kwargs.pop('edition')
        super().__init__(*args, **kwargs)

    def clean(self):
        super().clean()

        if not self.edition.get_setting('teams.registration.allowed').as_boolean():
            raise ValidationError('Team registration is not allowed at the moment.')

        if self.request.user.memberships.filter(team__edition=self.edition).exists():
            raise ValidationError('You already are a member of a team.')

    @transaction.atomic
    def save(self, *args, **kwargs):
        instance: Team = super().save(*args, **kwargs)

        # Check if the team limit has been reached
        if instance.edition.teams.count() > self.edition.get_setting('teams.limit').as_int():
            instance.status = Team.Status.BACKUP
            instance.save()

            messages.warning(self.request, 'The maximum amount of teams has been reached, but your team has been added to the backup list.')

        # Add current user to the team
        team_member = TeamMember(name=self.request.user.get_full_name(), user=self.request.user, team=instance)
        team_member.save()

        return instance


class ParticipantTeamUpdateForm(ModelForm):
    class Meta:
        model = Team
        fields = ('name', 'website', 'image')

    def __init__(self, *args, **kwargs):
        self.edition = kwargs.pop('edition')
        super().__init__(*args, **kwargs)

    def clean(self):
        super().clean()

        if not self.edition.get_setting('teams.edit.allowed').as_boolean():
            raise ValidationError('Team changes are not allowed at the moment.')


class ParticipantTeamPartialUpdateForm(ModelForm):
    class Meta:
        model = Team
        fields = ('website', )


class ParticipantTeamDeleteForm(Form):

    def __init__(self, *args, **kwargs):
        self.edition = kwargs.pop('edition')
        super().__init__(*args, **kwargs)

    def clean(self):
        super().clean()

        if not self.edition.get_setting('teams.edit.allowed').as_boolean():
            raise ValidationError('Team changes are not allowed at the moment.')


class ParticipantTeamJoinForm(ModelForm):
    class Meta:
        model = Team
        fields = ()

    join_code = forms.CharField(min_length=32, max_length=32, widget=HiddenInput())

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        self.edition = kwargs.pop('edition')
        super().__init__(*args, **kwargs)

    def clean(self):
        super().clean()

        if not self.edition.get_setting('teams.edit.allowed').as_boolean():
            raise ValidationError('Team changes are not allowed at the moment.')

        if self.instance.join_code != self.cleaned_data.get('join_code'):
            raise ValidationError('Invalid join code.', code='invalid_join_code')

        if self.instance.members.count() >= self.edition.get_setting('teams.members.limit').as_int():
            raise ValidationError('This team is full.')

        if self.instance.members.filter(user=self.request.user).exists():
            raise ValidationError('You already joined this team.')

    @transaction.atomic
    def save(self, *args, **kwargs):
        instance: Team = super().save(*args, **kwargs)

        # Add current user to the team
        team_member = TeamMember(name=self.request.user.get_full_name(), user=self.request.user, team=instance)
        team_member.save()

        return instance
