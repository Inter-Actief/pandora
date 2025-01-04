from django.db import models
from django.utils.translation import gettext_lazy as _

from .fields import UUID4Field


class BaseModel(models.Model):

    class Meta:
        abstract = True

    id = UUID4Field(_('ID'), primary_key=True)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)
