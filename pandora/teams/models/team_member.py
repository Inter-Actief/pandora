from typing import TYPE_CHECKING

from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse

from pandora.core.models import BaseModel
from pandora.teams.models.team import Team
from pandora.util import generate_random_string

if TYPE_CHECKING:
    from pandora.editions.models.day import Day


def _generate_team_member_code():
    return generate_random_string(64)


class TeamMember(BaseModel):

    name = models.CharField(max_length=255)
    code = models.CharField(max_length=64, unique=True, default=_generate_team_member_code)

    user = models.ForeignKey(User, related_name='memberships', on_delete=models.CASCADE)
    team = models.ForeignKey(Team, related_name='members', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def get_kill_code(self, day: 'Day'):
        return self.kill_codes.filter(day=day).first()

    @property
    def current_kill_code(self):
        if self.team.edition.current_day:
            return self.get_kill_code(self.team.edition.current_day)
        return None

    def get_kills(self, day: 'Day'):
        return self.kills.filter(code__day=day)

    @property
    def current_kills(self):
        if self.team.edition.current_day:
            return self.get_kills(self.team.edition.current_day)
        return self.kills.none()

    def get_kill_score(self, day: 'Day'):
        return self.get_kills(day).count() * self.team.edition.get_setting('kills.score').as_int()

    @property
    def current_kill_score(self):
        if self.team.edition.current_day:
            return self.get_kill_score(self.team.edition.current_day)
        return 0

    @property
    def total_kill_score(self):
        return self.kills.count() * self.team.edition.get_setting('kills.score').as_int()

    def get_absolute_url(self):
        return reverse('participant_team', kwargs={'year': self.team.edition.year, 'pk': self.team.id})

    def get_participant_update_url(self):
        return reverse('participant_team_member_update', kwargs={'year': self.team.edition.year, 'team_id': self.team.id, 'pk': self.id})

    def get_participant_delete_url(self):
        return reverse('participant_team_member_delete', kwargs={'year': self.team.edition.year, 'team_id': self.team.id, 'pk': self.id})
