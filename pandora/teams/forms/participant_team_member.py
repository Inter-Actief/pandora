from django.core.exceptions import ValidationError
from django.forms import Form
from django.forms.models import ModelForm

from pandora.editions.mixins import EditionMixin
from pandora.teams.models import TeamMember


class TeamMemberUpdateForm(EditionMixin, ModelForm):
    class Meta:
        model = TeamMember
        fields = ('name', )

    def __init__(self, *args, **kwargs):
        self.edition = kwargs.pop('edition')
        super().__init__(*args, **kwargs)

    def clean(self):
        super().clean()

        if not self.edition.get_setting('teams.edit.allowed').as_boolean():
            raise ValidationError('Team changes are not allowed at the moment.')


class TeamMemberDeleteForm(EditionMixin, Form):

    def __init__(self, *args, **kwargs):
        self.edition = kwargs.pop('edition')
        super().__init__(*args, **kwargs)

    def clean(self):
        super().clean()

        if not self.edition.get_setting('teams.edit.allowed').as_boolean():
            raise ValidationError('Team changes are not allowed at the moment.')
