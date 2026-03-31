from django.contrib.gis.forms import OSMWidget
from django.forms import ModelForm, HiddenInput

from pandora.puzzles.models import Puzzle


class PuzzleModelForm(ModelForm):

    class Meta:
        model = Puzzle
        fields = ('edition', 'name', 'solution', 'solution_direction', 'solution_distance', 'solution_description', 'location_point', 'location_description')
        widgets = {
            'edition': HiddenInput(),
            'location_point': OSMWidget()
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['location_point'].widget.attrs['geom_type'] = 'Point'
        self.fields['location_point'].widget.attrs['default_lat'] = '52.241972'
        self.fields['location_point'].widget.attrs['default_lon'] = '6.852272'
