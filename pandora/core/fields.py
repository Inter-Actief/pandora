from uuid import uuid4

from django.db.models.fields import UUIDField


class UUID4Field(UUIDField):

    def __init__(self, *args, **kwargs):
        kwargs['default'] = uuid4

        if kwargs['primary_key']:
            kwargs['editable'] = False

        super().__init__(*args, **kwargs)
