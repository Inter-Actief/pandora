from import_export.resources import ModelResource

from pandora.teams.models import TeamMember


class TeamMemberResource(ModelResource):
    class Meta:
        model = TeamMember
        fields = ('id', 'created_at', 'updated_at', 'user__email', 'user__first_name', 'user__last_name', 'name', 'team__name', 'team__status')
