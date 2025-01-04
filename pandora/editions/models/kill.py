from django.db import models

from pandora.core.models import BaseModel
from pandora.editions.models.kill_code import KillCode
from pandora.teams.models.team_member import TeamMember


class Kill(BaseModel):

    code = models.OneToOneField(KillCode, related_name='kill', on_delete=models.CASCADE)
    killer = models.ForeignKey(TeamMember, related_name='kills', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.killer.name} killed {self.victim.name} ({self.code.code})'

    @property
    def victim(self):
        return self.code.team_member
