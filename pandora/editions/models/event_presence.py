from django.db import models

from pandora.core.models import BaseModel
from pandora.editions.models.event import Event
from pandora.teams.models.team_member import TeamMember


class EventPresence(BaseModel):

    class Meta:
        unique_together = ('event', 'team_member')

    event = models.ForeignKey(Event, related_name='presences', on_delete=models.CASCADE)
    team_member = models.ForeignKey(TeamMember, related_name='presences', on_delete=models.CASCADE)

    def __str__(self):
        return f'Presence - {self.event.name} - {self.team_member.name}'

    def get_absolute_url(self):
        return self.event.get_absences_url()
