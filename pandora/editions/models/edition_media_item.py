from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models

from pandora.core.models import BaseModel
from pandora.editions.models.edition import Edition

YOUTUBE_URL_PREFIXES = (
    'https://youtube.com/',
    'https://www.youtube.com/',
    'https://youtu.be/',
)


def _get_edition_media_item_upload_path(edition_media_item: 'EditionMediaItem', filename: str):
    return f'edition-media-items/{str(edition_media_item.id)}/{filename}'


class EditionMediaItem(BaseModel):

    class Type(models.TextChoices):
        AUDIO = 'AUDIO', 'Audio',
        VIDEO = 'VIDEO', 'Video',
        OTHER = 'OTHER', 'Other'

    type = models.CharField(max_length=32, choices=Type.choices)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    url = models.URLField(blank=True)
    file = models.FileField(blank=True, null=True, upload_to=_get_edition_media_item_upload_path)
    is_hidden = models.BooleanField(default=True)
    sort_index = models.PositiveSmallIntegerField()

    edition = models.ForeignKey(Edition, related_name='media_items', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.edition.year} - {self.name}'

    @property
    def file_url(self):
        if not self.file:
            return None
        return f'{settings.PUBLIC_URL}{settings.MEDIA_URL}{self.file}'

    @property
    def youtube_url(self):
        if not self.url:
            return None

        for url_prefix in YOUTUBE_URL_PREFIXES:
            if self.url.startswith(url_prefix):
                return self.url.replace('/watch?v=', '/embed/')

        return None

    def clean(self):
        if (not self.url and not self.file) or (self.url and self.file):
            raise ValidationError('Edition media item requires either a URL of a file.', code='no_url_or_file')
