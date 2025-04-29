from django.urls import path

from .views import static as views
from .views.archive import ArchiveUploadView
from .views.committee_member import CommitteeMemberListView
from .views.dashboard import DashboardRedirectView, DashboardView, CommitteeDashboardView, CommitteeFeedDashboardView
from .views.edition import EditionCreateView, ParticipantEditionDetailView
from .views.edition_media_item import EditionMediaItemListView
from .views.edition_setting import EditionSettingListView, EditionSettingUpdateView
from .views.event import EventListView, EventAttendanceView, EventScannerView
from .views.event_absence import EventAbsenceCreateView, EventAbsenceListView, EventAbsenceUpdateView
from .views.event_presence import EventPresenceCreateView
from .views.kill import KillListView, KillCreateView
from .views.kill_code import KillCodeListView, KillCodeGenerateView, KillCodeExportView
from .views.score_modification import ScoreModificationCreateView, ScoreModificationDeleteView, ScoreModificationUpdateView
from .views.scores import ScoresTotalView, ScoresDayView, ScoresModificationsView, FeedView

urlpatterns = [
    path('', ParticipantEditionDetailView.as_view(), name='home'),
    path('<int:year>', ParticipantEditionDetailView.as_view(), name='participant_edition'),

    path('gameplay', views.gameplay, name='gameplay'),
    path('rules', views.rules, name='rules'),

    path('archive/upload', ArchiveUploadView.as_view(), name='archive_upload'),

    path('editions/add', EditionCreateView.as_view(), name='edition_create'),

    path('dashboard', DashboardRedirectView.as_view(), name='dashboard_redirect'),
    path('<int:year>/dashboard', DashboardView.as_view(), name='dashboard'),
    path('<int:year>/committee/dashboard', CommitteeDashboardView.as_view(), name='committee_dashboard'),
    path('<int:year>/committee/feed/dashboard', CommitteeFeedDashboardView.as_view(), name='committee_feed_dashboard'),

    path('<int:year>/scores', ScoresTotalView.as_view(), name='scores_total'),
    path('<int:year>/scores/days/<int:day_number>', ScoresDayView.as_view(), name='scores_day'),
    path('<int:year>/scores/modificiations', ScoresModificationsView.as_view(), name='scores_modifications'),
    path('<int:year>/feed', FeedView.as_view(), name='feed'),

    path('<int:year>/committee', CommitteeMemberListView.as_view(), name='committee'),

    path('<int:year>/media/<str:type>', EditionMediaItemListView.as_view(), name='edition_media'),

    path('<int:year>/teams/<uuid:team_id>/absences/add', EventAbsenceCreateView.as_view(), name='participant_event_absence_create'),

    path('<int:year>/kills/add', KillCreateView.as_view(), name='kill_add'),

    path('<int:year>/committee/settings', EditionSettingListView.as_view(), name='edition_settings'),
    path('<int:year>/committee/settings/<uuid:pk>/update', EditionSettingUpdateView.as_view(), name='edition_setting_update'),

    path('<int:year>/committee/events', EventListView.as_view(), name='events'),
    path('<int:year>/committee/events/<uuid:pk>/attendance', EventAttendanceView.as_view(), name='event_attendance'),
    path('<int:year>/committee/events/<uuid:pk>/scanner', EventScannerView.as_view(), name='event_scanner'),
    path('<int:year>/committee/events/<uuid:event_id>/absences', EventAbsenceListView.as_view(), name='event_absences'),
    path('<int:year>/committee/events/<uuid:event_id>/absences/<uuid:pk>', EventAbsenceUpdateView.as_view(), name='event_absence_update'),
    path('<int:year>/committee/events/<uuid:event_id>/presences/add', EventPresenceCreateView.as_view(), name='event_presence_add'),

    path('<int:year>/committee/kill-codes/generate', KillCodeGenerateView.as_view(), name='kill_code_generate'),
    path('<int:year>/committee/kill-codes/days/<int:day_number>', KillCodeListView.as_view(), name='kill_codes'),
    path('<int:year>/committee/kill-codes/days/<int:day_number>/export', KillCodeExportView.as_view(), name='kill_code_export'),

    path('<int:year>/committee/kills/days/<int:day_number>', KillListView.as_view(), name='kills'),

    path('<int:year>/commiteee/teams/<uuid:team_id>/score-modications/add', ScoreModificationCreateView.as_view(), name='score_modification_create'),
    path('<int:year>/commiteee/teams/<uuid:team_id>/score-modications/<uuid:pk>', ScoreModificationUpdateView.as_view(), name='score_modification_update'),
    path('<int:year>/commiteee/teams/<uuid:team_id>/score-modications/<uuid:pk>/delete', ScoreModificationDeleteView.as_view(), name='score_modification_delete'),
]
