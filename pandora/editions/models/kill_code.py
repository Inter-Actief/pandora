from django.db import models

from pandora.core.models import BaseModel
from pandora.editions.models.day import Day
from pandora.teams.models.team_member import TeamMember
from pandora.util import generate_random_string


def _generate_kill_code():
    return generate_random_string(10, digits=False)


class KillCode(BaseModel):

    class Meta:
        unique_together = (('day', 'code'), ('day', 'team_member'))

    code = models.CharField(max_length=32, default=_generate_kill_code)

    day = models.ForeignKey(Day, related_name='kill_codes', on_delete=models.CASCADE)
    team_member = models.ForeignKey(TeamMember, related_name='kill_codes', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.team_member.name} - Day {self.day.number} - {self.code}'

    @property
    def is_killed(self):
        return hasattr(self, 'kill') and self.kill
