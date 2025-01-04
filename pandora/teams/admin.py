from django.contrib.admin import register, ModelAdmin
from django.utils.html import format_html

from pandora.teams.models import Team, TeamMember


@register(Team)
class TeamAdmin(ModelAdmin):
    list_display = ('id', 'edition', 'status', 'name', 'website_url', 'join_url')
    list_filter = ('edition', )
    ordering = ('-edition__year', 'status', 'name')

    def website_url(self, team: Team):
        if not team.website:
            return None
        return format_html('<b><a href="{url}" target="website">{url}</a></b>', url=team.website)

    def join_url(self, team: Team):
        return format_html('<b><a href="{url}" target="join">Join link</a></b>', url=team.join_url)


@register(TeamMember)
class TeamMemberAdmin(ModelAdmin):
    list_display = ('id', 'team', 'user')
    list_filter = ('team', 'user')
