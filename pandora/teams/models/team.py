from typing import TYPE_CHECKING

from django.conf import settings
from django.db import models
from django.db.models import Sum, Count, Q, Max
from django.urls import reverse

from pandora.core.models import BaseModel
from pandora.util import generate_random_string

if TYPE_CHECKING:
    from pandora.editions.models.day import Day


def _generate_join_code():
    return generate_random_string(32, lowercase=True)


def _get_team_upload_path(team: 'Team', filename: str):
    return f'teams/{str(team.id)}/{filename}'


class Team(BaseModel):
    class Status(models.TextChoices):
        ACTIVE = 'ACTIVE', 'Active'
        BACKUP = 'BACKUP', 'Backup'

    class Meta:
        unique_together = ('edition', 'name')

    name = models.CharField(max_length=255)
    status = models.CharField(max_length=16, choices=Status.choices, default=Status.ACTIVE)
    website = models.URLField(max_length=255, blank=True, null=True)
    image = models.ImageField(blank=True, null=True, upload_to=_get_team_upload_path)
    join_code = models.CharField(max_length=32, default=_generate_join_code)

    # NOTE: Prevent circular import by using a string to define the relation
    edition = models.ForeignKey('editions.Edition', related_name='teams', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    @property
    def is_active(self):
        return self.status == Team.Status.ACTIVE

    @property
    def image_url(self):
        return f'{settings.PUBLIC_URL}{settings.MEDIA_URL}{self.image}' if hasattr(self, 'image') and self.image else None

    @property
    def join_url(self):
        url = reverse('participant_team_join', kwargs={'year': self.edition.year, 'pk': self.id, 'join_code': self.join_code})
        return f'{settings.PUBLIC_URL}{url}'

    def get_solves(self, day: 'Day'):
        return self.solves.filter(code__day=day)

    @property
    def current_solves(self):
        if self.edition.current_day:
            return self.get_solves(self.edition.current_day)
        return self.solves.none()

    def get_puzzle_score(self, day: 'Day'):
        return sum([solve.score for solve in self.get_solves(day).all()])

    @property
    def current_puzzle_score(self):
        if self.edition.current_day:
            return self.get_puzzle_score(self.edition.current_day)
        return 0

    @property
    def total_puzzle_score(self):
        return sum([self.get_puzzle_score(day) for day in self.edition.ordered_days])

    def get_bonus_solves(self):
        return self.solves.filter(code__day__isnull=True)

    @property
    def total_bonus_puzzle_score(self):
        return self.get_bonus_solves().count() * self.edition.get_setting('puzzles.score').as_int_list()[0]

    def get_puzzle_bonus_score(self, day: 'Day'):
        bonus_after = self.edition.get_setting('puzzles.bonus.after').as_int()
        bonus_scores = self.edition.get_setting('puzzles.bonus.score').as_int_list()

        solve_filter = Q(solves__code__day=day, solves__code__number__lte=bonus_after)

        teams_with_bonus = list(
            Team.objects
            .annotate(
                solve_count=Count('solves__code__number', filter=solve_filter),
                solve_created_at_max=Max('solves__created_at', filter=solve_filter)
            )
            .filter(solve_count__gte=bonus_after)
            .order_by('solve_created_at_max')
            .values_list('id', flat=True)
        )

        if self.id not in teams_with_bonus:
            return 0

        bonus_index = teams_with_bonus.index(self.id)
        return bonus_scores[min(bonus_index, len(bonus_scores) - 1)]

    @property
    def current_puzzle_bonus_score(self):
        if self.edition.current_day:
            return self.get_puzzle_bonus_score(self.edition.current_day)
        return 0

    @property
    def total_puzzle_bonus_score(self):
        return sum([self.get_puzzle_bonus_score(day) for day in self.edition.ordered_days])

    def get_hints(self, day: 'Day'):
        from pandora.puzzles.models import Hint

        return self.hints.filter(code__day=day).exclude(status=Hint.Status.CANCELED)

    def get_hint_score(self, day: 'Day'):
        return self.get_hints(day).count() * -self.edition.get_setting('puzzles.hint.score').as_int()

    @property
    def current_hint_score(self):
        if self.edition.current_day:
            return self.get_hint_score(self.edition.current_day)
        return 0

    @property
    def total_hint_score(self):
        from pandora.puzzles.models import Hint

        return self.hints.exclude(status=Hint.Status.CANCELED).count() * -self.edition.get_setting('puzzles.hint.score').as_int()

    def get_kill_score(self, day: 'Day'):
        from pandora.editions.models import Kill

        return Kill.objects.filter(killer__team=self, code__day=day).count() * self.edition.get_setting('kills.score').as_int()

    @property
    def current_kill_score(self):
        if self.edition.current_day:
            return self.get_kill_score(self.edition.current_day)
        return 0

    @property
    def total_kill_score(self):
        from pandora.editions.models import Kill

        return Kill.objects.filter(killer__team=self).count() * self.edition.get_setting('kills.score').as_int()

    @property
    def total_bonus_score(self):
        from pandora.editions.models import ArchiveScore, ScoreModification

        archive_score = self.archive_scores.filter(type=ArchiveScore.Type.BONUS).first()
        if archive_score:
            return archive_score.score

        bonus_score = self.score_modifications.filter(type=ScoreModification.Type.BONUS).aggregate(sum=Sum('amount'))['sum']
        return 0 if bonus_score is None else bonus_score

    @property
    def total_offence_score(self):
        from pandora.editions.models import ArchiveScore, ScoreModification

        archive_score = self.archive_scores.filter(type=ArchiveScore.Type.OFFENCE).first()
        if archive_score:
            return archive_score.score

        offence_score = self.score_modifications.filter(type=ScoreModification.Type.OFFENCE).aggregate(sum=Sum('amount'))['sum']
        return 0 if offence_score is None else offence_score

    @property
    def total_day_archive_score(self):
        from pandora.editions.models import ArchiveScore

        return self.archive_scores.filter(type=ArchiveScore.Type.DAY).aggregate(sum=Sum('score'))['sum']

    @property
    def total_other_archive_score(self):
        from pandora.editions.models import ArchiveScore

        archive_score = self.archive_scores.filter(type=ArchiveScore.Type.OTHER).first()
        return archive_score.score if archive_score else 0

    def get_score(self, day: 'Day'):
        from pandora.editions.models import ArchiveScore

        archive_score = self.archive_scores.filter(type=ArchiveScore.Type.DAY, day=day).first()
        if archive_score:
            return archive_score.score

        return self.get_puzzle_score(day) + self.get_puzzle_bonus_score(day) + self.get_hint_score(day) + self.get_kill_score(day)

    @property
    def current_score(self):
        if self.edition.current_day:
            return self.get_score(self.edition.current_day)
        return 0

    @property
    def total_score(self):
        from pandora.editions.models import ArchiveScore

        if self.edition.is_archive_scores:
            archive_score = self.archive_scores.filter(type=ArchiveScore.Type.TOTAL).first()
            if archive_score:
                return archive_score.score
            else:
                return self.total_day_archive_score + self.total_bonus_score + self.total_offence_score + self.total_other_archive_score

        return self.total_puzzle_score + self.total_puzzle_bonus_score + self.total_bonus_puzzle_score + self.total_hint_score + self.total_kill_score +\
            self.total_bonus_score + self.total_offence_score

    @property
    def table_total_puzzle_score(self):
        return self.total_puzzle_score + self.total_bonus_puzzle_score

    @property
    def table_total_bonus_score(self):
        return self.total_bonus_score + self.total_offence_score + self.total_bonus_puzzle_score

    def get_solve_numbers(self, day: 'Day'):
        return ', '.join([str(number) for number in self.solves.filter(code__day=day).order_by('code__number').values_list('code__number', flat=True)])

    @property
    def event_absences(self):
        from pandora.editions.models import EventAbsence

        return EventAbsence.objects.filter(team_member__team=self)

    def get_is_eliminated(self, day: 'Day'):
        from pandora.editions.models import KillCode

        return not KillCode.objects.filter(team_member__team=self, day=day, kill__isnull=True).exists()

    def get_absolute_url(self):
        return reverse('team', kwargs={'year': self.edition.year, 'pk': self.id})

    def get_score_modification_create_url(self):
        return reverse('score_modification_create', kwargs={'year': self.edition.year, 'team_id': self.id})

    def get_participant_url(self):
        return reverse('participant_team', kwargs={'year': self.edition.year, 'pk': self.id})

    def get_participant_update_url(self):
        return reverse('participant_team_update', kwargs={'year': self.edition.year, 'pk': self.id})

    def get_participant_partial_update_url(self):
        return reverse('participant_team_partial_update', kwargs={'year': self.edition.year, 'pk': self.id})

    def get_participant_delete_url(self):
        return reverse('participant_team_delete', kwargs={'year': self.edition.year, 'pk': self.id})
