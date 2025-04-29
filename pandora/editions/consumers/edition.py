from asgiref.sync import async_to_sync
from channels.generic.websocket import JsonWebsocketConsumer

from pandora.editions.models import Edition


class EditionFeedConsumer(JsonWebsocketConsumer):

    def _get_edition(self):
        return Edition.objects.get(id=self.scope['url_route']['kwargs']['edition_id'])

    def connect(self):
        edition = self._get_edition()
        async_to_sync(self.channel_layer.group_add)(edition.get_feed_channel_group(), self.channel_name)
        super().connect()

    def disconnect(self, code):
        edition = self._get_edition()
        async_to_sync(self.channel_layer.group_discard)(edition.get_feed_channel_group(), self.channel_name)
        super().disconnect(code)

    def send_message(self, message):
        edition = self._get_edition()
        if not edition.get_setting('scores.hidden').as_boolean() or edition.get_is_committee_member(self.scope['user']):
            # Send received group message to channel
            self.send_json(message)

    def send_committee_message(self, message):
        edition = self._get_edition()
        if edition.get_is_committee_member(self.scope['user']):
            # Send received group message to channel
            self.send_json(message)

    def solve(self, message):
        self.send_message(message)

    def puzzle_bonus(self, message):
        self.send_message(message)

    def completion(self, message):
        self.send_message(message)

    def kill(self, message):
        self.send_message(message)

    def elimination(self, message):
        self.send_message(message)

    def modification(self, message):
        self.send_message(message)

    def absence(self, message):
        self.send_committee_message(message)

    def hint(self, message):
        self.send_committee_message(message)
