from django.views.generic import ListView

from pandora.editions.mixins import EditionMixin
from pandora.editions.models import EditionMediaItem


class EditionMediaItemListView(EditionMixin, ListView):
    model = EditionMediaItem
    context_object_name = 'items'

    def get_queryset(self):
        queryset = self.edition.media_items.filter(is_hidden=False)

        if 'type' in self.kwargs:
            media_type = self.kwargs.get('type').upper()
            if media_type.endswith('S'):
                media_type = media_type[:-1]

            queryset = queryset.filter(type=media_type)

        return queryset.order_by('sort_index', 'name')

