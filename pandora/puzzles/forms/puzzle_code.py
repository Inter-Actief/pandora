from django.forms import ModelForm, HiddenInput

from pandora.puzzles.models import PuzzleCode, Puzzle


class PuzzleCodeModelForm(ModelForm):

    class Meta:
        model = PuzzleCode
        fields = ('puzzle', 'day', 'number')
        widgets = {
            'puzzle': HiddenInput()
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['day'].queryset = Puzzle.objects.get(id=self.initial['puzzle']).edition.days
