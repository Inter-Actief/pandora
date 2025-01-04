from pathlib import Path

from django.http import FileResponse
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView

from pandora.editions.mixins import CommitteeMemberAccessMixin, EditionMixin
from pandora.puzzles.forms.puzzle_file import PuzzleFileModelForm
from pandora.puzzles.models import PuzzleFile


class PuzzleFileCreateView(EditionMixin, CommitteeMemberAccessMixin, CreateView):
    model = PuzzleFile
    form_class = PuzzleFileModelForm
    template_name_suffix = '_create'

    def get_initial(self):
        initial = super().get_initial()
        initial['puzzle'] = self.kwargs['puzzle_id']
        return initial


class PuzzleFileUpdateView(EditionMixin, CommitteeMemberAccessMixin, UpdateView):
    model = PuzzleFile
    form_class = PuzzleFileModelForm
    context_object_name = 'puzzle_file'
    template_name_suffix = '_update'


class PuzzleFileDeleteView(EditionMixin, CommitteeMemberAccessMixin, DeleteView):
    model = PuzzleFile
    context_object_name = 'puzzle_file'
    template_name_suffix = '_delete'

    def get_success_url(self):
        return self.object.puzzle.get_absolute_url()


class PuzzleFileDownloadView(EditionMixin, DetailView):
    model = PuzzleFile

    object: PuzzleFile

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        path = Path(self.object.file.path)

        if self.object.type == PuzzleFile.Type.PUZZLE or self.object.type == PuzzleFile.Type.SOLUTION:
            if hasattr(self.object.puzzle, 'code') and self.object.puzzle.code:
                if self.object.puzzle.code.day:
                    prefix = f'{self.object.puzzle.edition.year} - Day {self.object.puzzle.code.day.number} - '
                else:
                    prefix = f'{self.object.puzzle.edition.year} - Bonus - '
            else:
                prefix = f'{self.object.puzzle.edition.year} - '

            suffix = ' - Solution' if self.object.type == PuzzleFile.Type.SOLUTION else ''

            return FileResponse(self.object.file, filename=f'{prefix}{self.object.puzzle.name}{suffix}{path.suffix}')

        return FileResponse(self.object.file, filename=f'{self.object.name}{path.suffix}')
