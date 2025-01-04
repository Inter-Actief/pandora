from django.contrib.admin import register, ModelAdmin

from pandora.pregames.models import Pregame, PregamePuzzleCode, PregameSolve


@register(Pregame)
class PregameAdmin(ModelAdmin):
    list_display = ('id', 'edition', 'start', 'end')
    list_filter = ('edition', 'start', 'end')
    ordering = ('-edition__year', '-start')


@register(PregamePuzzleCode)
class PregamePuzzleCodeAdmin(ModelAdmin):
    list_display = ('id', 'pregame', 'number', 'puzzle', 'code', 'created_at')
    list_filter = ('pregame', 'number', 'puzzle', 'created_at')


@register(PregameSolve)
class PregameSolveAdmin(ModelAdmin):
    list_display = ('id', 'team', 'puzzle', 'code', 'created_at')
    list_filter = ('team', 'created_at')
