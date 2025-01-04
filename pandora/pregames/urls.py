from django.urls import path

from .views.pregame import PregameScoresView
from .views.pregame_puzzle_code import PregamePuzzleCodeCreateView, PregamePuzzleCodeUpdateView, PregamePuzzleCodeDeleteView
from .views.pregame_solve import PregameSolveCreateView

urlpatterns = [
    path('<int:year>/committee/puzzles/<uuid:puzzle_id>/pregame-code/create', PregamePuzzleCodeCreateView.as_view(),
         name='pregame_puzzle_code_create'),
    path('<int:year>/committee/puzzles/<uuid:puzzle_id>/pregame-code/<uuid:pk>/update', PregamePuzzleCodeUpdateView.as_view(),
         name='pregame_puzzle_code_update'),
    path('<int:year>/committee/puzzles/<uuid:puzzle_id>/pregame-code/<uuid:pk>/delete', PregamePuzzleCodeDeleteView.as_view(),
         name='pregame_puzzle_code_delete'),

    path('<int:year>/scores/pregame', PregameScoresView.as_view(), name='pregame_scores'),

    path('<int:year>/pregames/solves/add', PregameSolveCreateView.as_view(), name='pregame_solve_add')
]
