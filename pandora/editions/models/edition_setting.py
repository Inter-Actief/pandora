from distutils.util import strtobool

from django.db import models
from django.urls import reverse

from pandora.core.models import BaseModel


class EditionSetting(BaseModel):

    class Meta:
        unique_together = ('edition', 'key')

    key = models.CharField(max_length=255)
    value = models.TextField(blank=True, null=True)

    edition = models.ForeignKey('editions.Edition', related_name='settings', blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        name = str(self.edition.year) if self.edition else 'Default'
        return f'{name} - {self.key}'

    @property
    def is_default(self):
        return self.edition is None

    @property
    def default_value(self):
        default_setting = EditionSetting.objects.filter(key=self.key, edition__isnull=True).first()
        return default_setting.value if default_setting else None

    def as_boolean(self):
        return strtobool(self.value)

    def as_int(self):
        return int(self.value)

    def as_str(self):
        return self.value

    def as_int_list(self):
        return [int(value) for value in self.value.split(',')]

    def get_absolute_url(self):
        return reverse('edition_settings', kwargs={'year': self.edition.year})

    def get_update_url(self):
        return reverse('edition_setting_update', kwargs={'year': self.edition.year, 'pk': self.id})
