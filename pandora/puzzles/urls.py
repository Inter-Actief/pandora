from django.urls import path

from .views.hint import HintCreateView, HintListView, HintDetailView, HintUpdateView, HintTeamDetailView, HintTeamCancelView
from .views.participant_puzzle_code import ParticipantPuzzleCodeListView
from .views.puzzle import PuzzleListView, PuzzleCreateView, PuzzleDetailView, PuzzleUpdateView, PuzzleDeleteView
from .views.puzzle_code import PuzzleCodeCreateView, PuzzleCodeUpdateView, PuzzleCodeDeleteView
from .views.puzzle_file import PuzzleFileCreateView, PuzzleFileUpdateView, PuzzleFileDeleteView, PuzzleFileDownloadView
from .views.solve import SolveCreateView, SolveListView

urlpatterns = [
    path('<int:year>/committee/puzzles', PuzzleListView.as_view(), name='puzzles'),
    path('<int:year>/committee/puzzles/add', PuzzleCreateView.as_view(), name='puzzle_create'),
    path('<int:year>/committee/puzzles/<uuid:pk>', PuzzleDetailView.as_view(), name='puzzle'),
    path('<int:year>/committee/puzzles/<uuid:pk>/update', PuzzleUpdateView.as_view(), name='puzzle_update'),
    path('<int:year>/committee/puzzles/<uuid:pk>/delete', PuzzleDeleteView.as_view(), name='puzzle_delete'),

    path('<int:year>/committee/puzzles/<uuid:puzzle_id>/code/create', PuzzleCodeCreateView.as_view(), name='puzzle_code_create'),
    path('<int:year>/committee/puzzles/<uuid:puzzle_id>/code/<uuid:pk>/update', PuzzleCodeUpdateView.as_view(), name='puzzle_code_update'),
    path('<int:year>/committee/puzzles/<uuid:puzzle_id>/code/<uuid:pk>/delete', PuzzleCodeDeleteView.as_view(), name='puzzle_code_delete'),

    path('<int:year>/committee/puzzles/<uuid:puzzle_id>/files/create', PuzzleFileCreateView.as_view(), name='puzzle_file_create'),
    path('<int:year>/committee/puzzles/<uuid:puzzle_id>/files/<uuid:pk>/update', PuzzleFileUpdateView.as_view(), name='puzzle_file_update'),
    path('<int:year>/committee/puzzles/<uuid:puzzle_id>/files/<uuid:pk>/delete', PuzzleFileDeleteView.as_view(), name='puzzle_file_delete'),

    path('<int:year>/committee/solves/days/<int:day_number>', SolveListView.as_view(), name='solves'),
    path('<int:year>/committee/solves/bonus', SolveListView.as_view(), name='solves_bonus'),

    path('<int:year>/committee/hints', HintListView.as_view(), name='hints'),
    path('<int:year>/committee/hints/<uuid:pk>', HintDetailView.as_view(), name='hint'),
    path('<int:year>/committee/hints/<uuid:pk>/update', HintUpdateView.as_view(), name='hint_update'),

    path('<int:year>/puzzles', ParticipantPuzzleCodeListView.as_view(), name='participant_puzzle_codes'),

    path('<int:year>/puzzles/downloads/<uuid:pk>', PuzzleFileDownloadView.as_view(), name='puzzle_file_download'),

    path('<int:year>/solves/add', SolveCreateView.as_view(), name='solve_add'),

    path('<int:year>/hints/add', HintCreateView.as_view(), name='hint_add'),
    path('<int:year>/hints/<uuid:pk>', HintTeamDetailView.as_view(), name='hint_team'),
    path('<int:year>/hints/<uuid:pk>/cancel', HintTeamCancelView.as_view(), name='hint_team_cancel')
]
