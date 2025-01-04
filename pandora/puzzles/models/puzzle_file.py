import os

from django.contrib.gis.db import models
from django.urls import reverse

from pandora.core.models import BaseModel


def _get_puzzle_file_upload_path(puzzle_file: 'PuzzleFile', filename: str):
    return f'puzzle-files/{str(puzzle_file.id)}/{filename}'


class PuzzleFile(BaseModel):

    class Type(models.TextChoices):
        PUZZLE = 'PUZZLE'
        SOLUTION = 'SOLUTION'
        OTHER = 'OTHER'

    class Meta:
        unique_together = ('puzzle', 'name')

    type = models.CharField(max_length=32, choices=Type.choices)
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to=_get_puzzle_file_upload_path)

    puzzle = models.ForeignKey('puzzles.Puzzle', related_name='files', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.puzzle.edition.year} - {self.puzzle.name} - {self.name}'

    @property
    def file_name(self):
        return os.path.basename(self.file.name)

    def get_absolute_url(self):
        return reverse('puzzle', kwargs={'year': self.puzzle.edition.year, 'pk': self.puzzle_id})

    def get_update_url(self):
        return reverse('puzzle_file_update', kwargs={'year': self.puzzle.edition.year, 'puzzle_id': self.puzzle.id, 'pk': self.id})

    def get_delete_url(self):
        return reverse('puzzle_file_delete', kwargs={'year': self.puzzle.edition.year, 'puzzle_id': self.puzzle.id, 'pk': self.id})

    def get_download_url(self):
        return reverse('puzzle_file_download', kwargs={'year': self.puzzle.edition.year, 'pk': self.id})
