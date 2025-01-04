from django.urls import path

from .views.participant_team import ParticipantTeamListView, ParticipantTeamCreateView, ParticipantTeamDetailView, ParticipantTeamUpdateView,\
    ParticipantTeamPartialUpdateView, ParticipantTeamDeleteView, ParticipantTeamJoinView
from .views.participant_team_member import TeamMemberParticipantUpdateView, TeamMemberParticipantDeleteView
from .views.team import TeamListView, TeamDetailView
from .views.team_member import TeamMemberExportView

urlpatterns = [
    path('<int:year>/committee/teams', TeamListView.as_view(), name='teams'),
    path('<int:year>/committee/teams/<uuid:pk>', TeamDetailView.as_view(), name='team'),
    path('<int:year>/committee/team-members/export', TeamMemberExportView.as_view(), name='team_member_export'),

    path('<int:year>/teams', ParticipantTeamListView.as_view(), name='participant_teams'),
    path('<int:year>/teams/add/', ParticipantTeamCreateView.as_view(), name='participant_team_add'),
    path('<int:year>/teams/<uuid:pk>', ParticipantTeamDetailView.as_view(), name='participant_team'),
    path('<int:year>/teams/<uuid:pk>/update', ParticipantTeamUpdateView.as_view(), name='participant_team_update'),
    path('<int:year>/teams/<uuid:pk>/update/partial', ParticipantTeamPartialUpdateView.as_view(), name='participant_team_partial_update'),
    path('<int:year>/teams/<uuid:pk>/delete', ParticipantTeamDeleteView.as_view(), name='participant_team_delete'),
    path('<int:year>/teams/<uuid:pk>/join/<str:join_code>', ParticipantTeamJoinView.as_view(), name='participant_team_join'),

    path('<int:year>/teams/<uuid:team_id>/members/<uuid:pk>/update', TeamMemberParticipantUpdateView.as_view(), name='participant_team_member_update'),
    path('<int:year>/teams/<uuid:team_id>/members/<uuid:pk>/delete', TeamMemberParticipantDeleteView.as_view(), name='participant_team_member_delete'),
]
