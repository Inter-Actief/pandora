from uuid import uuid4

from django.db.models.fields import UUIDField


class UUID4Field(UUIDField):

    def __init__(self, *args, **kwargs):
        kwargs['default'] = uuid4

        if kwargs['primary_key']:
            kwargs['editable'] = False

        super().__init__(*args, **kwargs)

    def db_type(self, connection):
        return "char(32)"

    def get_db_prep_value(self, value, connection, prepared=False):
        value = super().get_db_prep_value(value, connection, prepared)
        if value is None:
            return None
        return value.hex
