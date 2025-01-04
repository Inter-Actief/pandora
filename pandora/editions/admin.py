from django.contrib.admin import register, ModelAdmin
from django.utils.html import format_html

from pandora.editions.models import Edition, EditionSetting, EditionMediaItem, CommitteeMember, Day, Event, EventPresence, EventAbsence, KillCode, Kill, \
    ScoreModification, ArchiveScore


@register(Edition)
class EditionAdmin(ModelAdmin):
    list_display = ('id', 'year', 'name', 'is_hidden')
    list_filter = ('is_hidden', )
    ordering = ('-year', )


@register(EditionSetting)
class EditionSettingAdmin(ModelAdmin):
    list_display = ('id', 'edition', 'key', 'value')
    list_filter = ('edition', )
    ordering = ('-edition__year', 'key')


@register(EditionMediaItem)
class EditionMediaItemAdmin(ModelAdmin):
    list_display = ('id', 'edition', 'is_hidden', 'sort_index', 'name', 'link')
    list_filter = ('edition', 'is_hidden')
    ordering = ('-edition__year', 'is_hidden', 'sort_index')

    def link(self, item: EditionMediaItem):
        return format_html('<b><a href="{url}" target="media">Link</a></b>', url=item.file_url if item.file else item.url)


@register(CommitteeMember)
class CommitteeMemberAdmin(ModelAdmin):
    list_display = ('id', 'edition', 'is_hidden', 'sort_index', 'function', 'name', 'user',)
    list_filter = ('edition', 'function', 'is_hidden')
    ordering = ('-edition__year', 'is_hidden', 'sort_index')


@register(Day)
class DayAdmin(ModelAdmin):
    list_display = ('id', 'edition', 'number', 'start', 'end')
    list_filter = ('edition', 'number', 'start', 'end')
    ordering = ('-edition__year', 'number')


@register(Event)
class EventAdmin(ModelAdmin):
    list_display = ('id', 'edition', 'name', 'start', 'end')
    list_filter = ('edition', 'name', 'start', 'end')
    ordering = ('-edition__year', 'start')


@register(EventPresence)
class EventPresenceAdmin(ModelAdmin):
    list_display = ('id', 'event', 'team_member', 'created_at')
    list_filter = ('event', 'team_member', 'created_at')


@register(EventAbsence)
class EventAbsenceAdmin(ModelAdmin):
    list_display = ('id', 'event', 'team_member', 'status', 'created_at')
    list_filter = ('status', 'event', 'team_member', 'created_at')


@register(KillCode)
class KillCodeAdmin(ModelAdmin):
    list_display = ('id', 'day', 'team_member', 'code', 'created_at')
    list_filter = ('day', 'team_member', 'created_at')


@register(Kill)
class KillAdmin(ModelAdmin):
    list_display = ('id', 'killer', 'victim', 'code', 'created_at')
    list_filter = ('killer', 'created_at')


@register(ScoreModification)
class ScoreModificationAdmin(ModelAdmin):
    list_display = ('id', 'team', 'type', 'amount', 'reason', 'team_member', 'created_at')
    list_filter = ('type', 'team', 'team_member', 'created_at')


@register(ArchiveScore)
class ArchiveScoreAdmin(ModelAdmin):
    list_display = ('id', 'team', 'type', 'score', 'day')
    list_filter = ('type', 'team', 'day')
