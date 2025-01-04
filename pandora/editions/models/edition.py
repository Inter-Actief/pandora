from typing import Optional, TYPE_CHECKING

from django.contrib.auth.models import User
from django.db import models
from django.db.models import Max
from django.template.loader import select_template
from django.urls import reverse
from django.utils import timezone
from django_request_cache import cache_for_request

from pandora.core.models import BaseModel
from pandora.editions.models.edition_setting import EditionSetting
from pandora.teams.models.team import Team
from pandora.teams.models.team_member import TeamMember

if TYPE_CHECKING:
    from pandora.pregames.models import PregamePuzzleCode
    from pandora.puzzles.models import PuzzleCode


class Edition(BaseModel):

    class Meta:
        get_latest_by = 'year'
        unique_together = ('year', )

    # If there are ever multiple Pandora's in one year, a month or week field could be added. Note to also update `get_latest_by` and `unique_together` above.
    year = models.PositiveSmallIntegerField()
    name = models.CharField(max_length=255)
    is_hidden = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.year} - {self.name}'

    @property
    def start_day(self):
        return self.days.order_by('number').first()

    @property
    def end_day(self):
        return self.days.order_by('number').last()

    # TODO: cache_for_request works on a global level instead, so it should be modified to take self into account

    @property
    @cache_for_request
    def ordered_days(self):
        return self.days.order_by('number').all()

    @property
    @cache_for_request
    def current_day(self):
        now = timezone.now()
        queryset = self.days.filter(start__lte=now, end__gt=now)
        if queryset.count() != 1:
            return None
        return queryset.first()

    @property
    @cache_for_request
    def next_day(self):
        now = timezone.now()
        return self.days.filter(start__gt=now, end__gt=now).order_by('start').first()

    @property
    def start(self):
        return self.start_day.start

    @property
    def end(self):
        return self.end_day.end

    @property
    def is_ended(self):
        if not self.end_day:
            return True
        now = timezone.now()
        return now >= self.end

    @property
    def is_archive_scores(self):
        from pandora.editions.models import ArchiveScore

        return ArchiveScore.objects.filter(team__edition=self).count() > 0

    @property
    def has_day_archive_scores(self):
        from pandora.editions.models import ArchiveScore

        return ArchiveScore.objects.filter(type=ArchiveScore.Type.DAY, team__edition=self).count() > 0

    @property
    def has_modification_archive_scores(self):
        from pandora.editions.models import ArchiveScore

        return ArchiveScore.objects.filter(type__in=(ArchiveScore.Type.BONUS, ArchiveScore.Type.OFFENCE), team__edition=self).count() > 0

    @property
    def has_other_archive_scores(self):
        from pandora.editions.models import ArchiveScore

        return ArchiveScore.objects.filter(type=ArchiveScore.Type.OTHER, team__edition=self).count() > 0

    @property
    def hype_drink_event(self):
        return self.events.filter(name__exact='Hype Drink').first()

    @property
    def is_before_hype_drink_event(self):
        return timezone.now() < self.hype_drink_event.start if self.hype_drink_event else False

    @property
    def current_events(self):
        now = timezone.now()
        return self.events.filter(start__lte=now, end__gt=now, is_hidden=False).order_by('start', 'name').all()

    @property
    def next_events(self):
        now = timezone.now()

        queryset = self.events.filter(start__gt=now, end__gt=now, is_hidden=False).order_by('start', 'name')
        next_event = queryset.first()
        if next_event:
            return queryset.filter(start=next_event.start).all()
        return queryset.none()

    @property
    def active_teams(self):
        return self.teams.filter(status=Team.Status.ACTIVE)

    @property
    def team_members(self):
        return TeamMember.objects.filter(team__edition=self)

    @property
    def active_team_members(self):
        return TeamMember.objects.filter(team__edition=self, team__status=Team.Status.ACTIVE)

    @property
    def url_day_number(self):
        day = self.current_day
        return day.number if day else 1

    @property
    def is_scores_hidden(self):
        return self.get_setting('scores.hidden').as_boolean()

    @property
    def is_theme_hidden(self):
        return self.get_setting('theme.hidden').as_boolean()

    @property
    def theme_favicon_file(self):
        return f'images/themes/{self.year}/favicon.png'

    @property
    def theme_css_files(self):
        return [
            f'css/themes/{self.year}/bootstrap.css',
            f'css/themes/{self.year}/main.css'
        ]

    @property
    def theme_logo_file(self):
        return f'images/themes/{self.year}/logo.png'

    @property
    def theme_committee_image_file(self):
        return f'images/themes/{self.year}/photos/committee.jpg'

    @property
    def theme_background_template(self):
        return select_template([f'themes/{self.year}/background.html', 'themes/general/background.html'])

    @property
    def theme_header_template(self):
        return select_template([f'themes/{self.year}/header.html', 'themes/general/header.html'])

    @property
    def theme_footer_template(self):
        return select_template([f'themes/{self.year}/footer.html', 'themes/general/footer.html'])

    @property
    def theme_page_title_start_template(self):
        return select_template([f'themes/{self.year}/page_title_start.html', 'themes/general/page_title_start.html'])

    @property
    def theme_page_title_end_template(self):
        return select_template([f'themes/{self.year}/page_title_end.html', 'themes/general/page_title_end.html'])

    @property
    def bonus_puzzle_codes(self):
        from pandora.puzzles.models import PuzzleCode

        return PuzzleCode.objects.filter(puzzle__edition=self, day__isnull=True)

    @property
    def puzzle_code_day_count(self):
        return 2 + self.days.count()

    @property
    def puzzle_code_numbers(self):
        from pandora.puzzles.models import PuzzleCode

        max_number = self.days.aggregate(max=Max('puzzle_codes__number'))['max']
        max_bonus_number = PuzzleCode.objects.filter(puzzle__edition=self, day__isnull=True).aggregate(max=Max('number'))['max']
        max_pregame_number = self.pregame.puzzle_codes.aggregate(max=Max('number'))['max'] if self.pregame else 0
        return range(1, 1 + max([x for x in [0, max_number, max_bonus_number, max_pregame_number] if x is not None]))

    @cache_for_request
    # TODO: see above
    def get_setting(self, key: str):
        setting = self.settings.filter(key=key).first()
        if setting:
            return setting

        return EditionSetting.objects.filter(key=key, edition__isnull=True).get()

    def get_is_committee_member(self, user: User):
        return user.is_authenticated and user.committee_memberships.filter(edition=self).exists()

    # def get_absolute_url(self):
    #     return reverse('edition', kwargs={'pk': self.id})

    def get_participant_scores_url(self):
        if hasattr(self, 'pregame') and self.pregame and self.pregame.is_active:
            return reverse('pregame_scores', kwargs={'year': self.year})
        if self.current_day:
            return reverse('scores_day', kwargs={'year': self.year, 'day_number': self.current_day.number})
        return reverse('scores_total', kwargs={'year': self.year})

    def get_media_url(self):
        if self.is_ended:
            return reverse('participant_puzzle_codes', kwargs={'year': self.year})
        return reverse('edition_media', kwargs={'year': self.year, 'type': 'videos'})

    def get_puzzles_url(self):
        return reverse('puzzles', kwargs={'year': self.year})

    def get_settings_url(self):
        return reverse('edition_settings', kwargs={'year': self.year})

    def get_kill_codes_url(self):
        return reverse('kill_codes', kwargs={'year': self.year, 'day_number': 1})

    def get_kill_code_generate_url(self):
        return reverse('kill_code_generate', kwargs={'year': self.year})

    def get_team_member_export_url(self):
        return reverse('team_member_export', kwargs={'year': self.year})

    def get_feed_channel_group(self):
        return f'edition.{str(self.id)}.feed'

    def get_pregame_puzzle_code(self, number: int) -> Optional['PregamePuzzleCode']:
        return self.pregame.puzzle_codes.filter(number=number).first() if self.pregame else None

    def get_bonus_puzzle_code(self, number: int) -> Optional['PuzzleCode']:
        return self.bonus_puzzle_codes.filter(number=number).first()

    @staticmethod
    @cache_for_request
    def get_latest():
        return Edition.objects.filter(is_hidden=False).latest()
