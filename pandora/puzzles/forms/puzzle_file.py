from django.forms import ModelForm, HiddenInput

from pandora.puzzles.models import PuzzleFile


class PuzzleFileModelForm(ModelForm):

    class Meta:
        model = PuzzleFile
        fields = ('puzzle', 'type', 'name', 'file')
        widgets = {
            'puzzle': HiddenInput()
        }
