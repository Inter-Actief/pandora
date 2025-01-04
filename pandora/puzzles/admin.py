from django.contrib.admin import register, ModelAdmin
from django.contrib.gis.admin import GISModelAdmin
from django.utils.html import format_html

from pandora.puzzles.models import Puzzle, PuzzleFile, PuzzleCode, Solve, Hint


@register(Puzzle)
class PuzzleAdmin(GISModelAdmin):
    list_display = ('id', 'edition', 'name')
    list_filter = ('edition', )
    ordering = ('-edition__year', 'name')


@register(PuzzleFile)
class PuzzleFileAdmin(ModelAdmin):
    list_display = ('id', 'puzzle', 'type', 'name', 'link')
    list_filter = ('type', )
    ordering = ('-puzzle__edition__year', 'puzzle__name', '-type', 'name')

    def link(self, puzzle_file: PuzzleFile):
        return format_html('<b><a href="{url}" target="puzzle-file">Link</a></b>', url=puzzle_file.get_download_url())


@register(PuzzleCode)
class PuzzleCodeAdmin(ModelAdmin):
    list_display = ('id', 'day', 'number', 'puzzle', 'code', 'created_at')
    list_filter = ('day', 'number', 'puzzle', 'created_at')


@register(Solve)
class SolveAdmin(ModelAdmin):
    list_display = ('id', 'team', 'puzzle', 'code', 'created_at')
    list_filter = ('team', 'created_at')


@register(Hint)
class HintAdmin(ModelAdmin):
    list_display = ('id', 'team', 'code', 'status', 'created_at')
    list_filter = ('status', 'team', 'created_at')
