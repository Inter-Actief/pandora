from django.db import models
from django.urls import reverse
from django.utils import timezone

from pandora.core.models import BaseModel
from pandora.editions.models.edition import Edition
from pandora.editions.models.event_absence import EventAbsence
from pandora.teams.models.team_member import TeamMember


class Event(BaseModel):

    class Meta:
        unique_together = ('edition', 'name')

    name = models.CharField(max_length=255)
    start = models.DateTimeField()
    end = models.DateTimeField()
    is_hidden = models.BooleanField(default=False)

    edition = models.ForeignKey(Edition, related_name='events', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.edition.year} - {self.name}'

    @property
    def should_display_full(self):
        return (self.end - self.start).days >= 1 or (self.start - timezone.now()).days >= 1

    @property
    def formatted_name(self):
        return '{name} - {start:%A} {start.day} {start:%B} {start.year}'.format(name=self.name, start=self.start)

    @property
    def present_team_members(self):
        return TeamMember.objects.filter(presences__event=self).order_by('user__first_name', 'user__last_name')

    @property
    def absent_team_members(self):
        return TeamMember.objects.filter(absences__event=self, absences__status=EventAbsence.Status.APPROVED).order_by('user__first_name', 'user__last_name')

    @property
    def missing_team_members(self):
        present_ids = self.present_team_members.values_list('id', flat=True)
        absent_ids = self.absent_team_members.values_list('id', flat=True)
        return self.edition.active_team_members.exclude(id__in=[*present_ids, *absent_ids]).order_by('user__first_name', 'user__last_name')

    def get_absolute_url(self):
        return None

    def get_absences_url(self):
        return reverse('event_absences', kwargs={'year': self.edition.year, 'event_id': self.id})

    def get_attendance_url(self):
        return reverse('event_attendance', kwargs={'year': self.edition.year, 'pk': self.id})

    def get_scanner_url(self):
        return reverse('event_scanner', kwargs={'year': self.edition.year, 'pk': self.id})

    def get_member_search_url(self):
        return reverse('event_presence_add', kwargs={'year': self.edition.year, 'event_id': self.id})

    def get_scanner_channel_group(self):
        return f'event.{str(self.id)}.scanner'
