from django.contrib.gis.db import models
from django.urls import reverse

from pandora.core.models import BaseModel
from pandora.editions.models.edition import Edition
from pandora.puzzles.models.puzzle_file import PuzzleFile


class Puzzle(BaseModel):

    class Direction(models.TextChoices):
        NONE = 'NONE', 'None'
        NORTH_WEST = 'NORTH_WEST', 'North-West'
        NORTH = 'NORTH', 'North'
        NORTH_EAST = 'NORTH_EAST', 'North-East'
        EAST = 'EAST', 'East'
        SOUTH_EAST = 'SOUTH_EAST', 'South-East'
        SOUTH = 'SOUTH', 'South'
        SOUTH_WEST = 'SOUTH_WEST', 'South-West'
        WEST = 'WEST', 'West'

    name = models.CharField(max_length=255)
    solution = models.CharField(max_length=255, blank=True)
    solution_direction = models.CharField(max_length=16, choices=Direction.choices)
    solution_distance = models.PositiveSmallIntegerField(blank=True, null=True, help_text="Distance in meters between the solution and the puzzle code. "
                                                                                          "Should be left blank most of the time.")
    solution_description = models.TextField(blank=True)
    location_point = models.PointField(blank=True, null=True)
    location_description = models.TextField(blank=True)

    edition = models.ForeignKey(Edition, related_name='puzzles', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.edition.year} - {self.name}'

    @property
    def puzzle_file(self):
        return self.files.filter(type=PuzzleFile.Type.PUZZLE).order_by('-created_at').first()

    @property
    def non_puzzle_files(self):
        return self.files.exclude(type=PuzzleFile.Type.PUZZLE).order_by('type', 'name')

    def get_absolute_url(self):
        return reverse('puzzle', kwargs={'year': self.edition.year, 'pk': self.id})

    def get_update_url(self):
        return reverse('puzzle_update', kwargs={'year': self.edition.year, 'pk': self.id})

    def get_delete_url(self):
        return reverse('puzzle_delete', kwargs={'year': self.edition.year, 'pk': self.id})

    def get_code_create_url(self):
        return reverse('puzzle_code_create', kwargs={'year': self.edition.year, 'puzzle_id': self.id})

    def get_pregame_code_create_url(self):
        return reverse('pregame_puzzle_code_create', kwargs={'year': self.edition.year, 'puzzle_id': self.id})

    def get_file_create_url(self):
        return reverse('puzzle_file_create', kwargs={'year': self.edition.year, 'puzzle_id': self.id})
