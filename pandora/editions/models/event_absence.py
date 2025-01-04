from django.db import models
from django.urls import reverse

from pandora.core.models import BaseModel
from pandora.teams.models.team_member import TeamMember


class EventAbsence(BaseModel):

    class Status(models.TextChoices):
        WAITING = 'WAITING'
        APPROVED = 'APPROVED'
        DECLINED = 'DECLINED'

    class Meta:
        unique_together = ('event', 'team_member')

    status = models.CharField(max_length=32, choices=Status.choices, default=Status.WAITING)
    reason = models.TextField()
    feedback = models.TextField(blank=True, null=True)

    event = models.ForeignKey('editions.Event', related_name='absences', on_delete=models.CASCADE)
    team_member = models.ForeignKey(TeamMember, related_name='absences', on_delete=models.CASCADE)

    def __str__(self):
        return f'Absence - {self.event.name} - {self.team_member.name}'

    def get_absolute_url(self):
        return self.event.get_absences_url()

    def get_update_url(self):
        return reverse('event_absence_update', kwargs={'year': self.event.edition.year, 'event_id': self.event.id, 'pk': self.id})
