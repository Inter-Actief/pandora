from import_export.resources import ModelResource

from pandora.editions.models import KillCode


class KillCodeResource(ModelResource):
    class Meta:
        model = KillCode
        fields = ('id', 'created_at', 'updated_at', 'day__number', 'team_member__team__name', 'team_member__name', 'code')
