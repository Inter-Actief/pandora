from django.forms import ModelForm, HiddenInput

from pandora.pregames.models import PregamePuzzleCode


class PregamePuzzleCodeModelForm(ModelForm):

    class Meta:
        model = PregamePuzzleCode
        fields = ('pregame', 'puzzle', 'number')
        widgets = {
            'pregame': HiddenInput(),
            'puzzle': HiddenInput()
        }
