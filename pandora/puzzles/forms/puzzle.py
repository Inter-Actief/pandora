from django.forms import ModelForm, HiddenInput

from pandora.puzzles.models import Puzzle


class PuzzleModelForm(ModelForm):

    class Meta:
        model = Puzzle
        fields = ('edition', 'name', 'solution', 'solution_direction', 'solution_distance', 'solution_description', 'location_point', 'location_description')
        widgets = {
            'edition': HiddenInput()
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # TODO: figure out why location_position widget is different from the admin widget (gis/forms/widgets.py vs gis/admin/widgets.py)
