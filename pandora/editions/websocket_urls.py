from django.urls import path

from pandora.editions.consumers.edition import EditionFeedConsumer
from pandora.editions.consumers.event import EventScannerConsumer

urlpatterns = [
    path('editions/<uuid:edition_id>/feed', EditionFeedConsumer.as_asgi(), name='edition_feed'),

    path('editions/<uuid:edition_id>/events/<uuid:event_id>/scanner', EventScannerConsumer.as_asgi(), name='event_scanner')
]
