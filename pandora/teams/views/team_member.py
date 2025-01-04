from django.http import HttpResponse
from django.views.generic import View

from pandora.editions.mixins import CommitteeMemberAccessMixin, EditionMixin
from pandora.teams.resources.team_member import TeamMemberResource


class TeamMemberExportView(EditionMixin, CommitteeMemberAccessMixin, View):

    def get(self, request, *args, **kwargs):
        dataset = TeamMemberResource().export(self.edition.team_members.order_by('team__name', 'name'))

        file_name = f'{self.edition.year}_team_members.csv'
        file_content = dataset.csv

        response = HttpResponse(file_content, content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename={file_name}'
        return response
