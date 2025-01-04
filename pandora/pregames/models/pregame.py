from django.db import models
from django.utils import timezone

from pandora.core.models import BaseModel
from pandora.editions.models.edition import Edition


class Pregame(BaseModel):

    start = models.DateTimeField()
    end = models.DateTimeField()
    bonus_amount = models.SmallIntegerField()
    bonus_reason = models.TextField()

    edition = models.OneToOneField(Edition, related_name='pregame', on_delete=models.CASCADE)

    def __str__(self):
        return f'Pregame {self.edition.year}'

    @property
    def is_before(self):
        return timezone.now() < self.start

    @property
    def is_active(self):
        return self.start <= timezone.now() < self.end

    @property
    def first_puzzle(self):
        puzzle_code = self.puzzle_codes.order_by('number').first()
        return puzzle_code.puzzle if puzzle_code else None
