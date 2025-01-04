from django.contrib.auth.models import User
from django.db import models

from pandora.core.models import BaseModel
from pandora.editions.models.edition import Edition


class CommitteeMember(BaseModel):

    name = models.CharField(max_length=255)
    function = models.CharField(max_length=255)
    sort_index = models.PositiveSmallIntegerField()
    is_hidden = models.BooleanField(default=False)

    user = models.ForeignKey(User, related_name='committee_memberships', blank=True, null=True, on_delete=models.CASCADE)
    edition = models.ForeignKey(Edition, related_name='committee_members', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.edition.year} - {self.function} - {self.name}'
