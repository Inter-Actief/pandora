import unicodedata
from collections.abc import Callable
from typing import Any, Optional

from django.forms import Select


class FormattedSelect(Select):

    format_label: Optional[Callable[[Any], str]] = None

    def __init__(self, *args, format_label: Callable[[Any], str] = None, **kwargs):
        super().__init__(*args, **kwargs)
        self.format_label = format_label

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)

        for group_name, group_choices, group_index in context['widget']['optgroups']:
            for option in group_choices:
                if option['value'] == '':
                    continue

                option['label'] = self.format_label(option['value'].instance) if self.format_label else option['label']

        return context


class SearchableSelect(Select):

    input_type = 'input'
    template_name = 'widgets/searchable_select.html'
    option_template_name = 'widgets/searchable_select_option.html'

    format_label: Optional[Callable[[Any], str]] = None

    def __init__(self, *args, format_label: Callable[[Any], str] = None, **kwargs):
        super().__init__(*args, **kwargs)
        self.format_label = format_label

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)

        context['input_id'] = context['widget']['attrs']['id']
        context['data_id'] = context['widget']['attrs']['id'] + '_data'

        context['data'] = []
        for group_name, group_choices, group_index in context['widget']['optgroups']:
            for option in group_choices:
                if option['value'] == '':
                    continue

                label = self.format_label(option['value'].instance) if self.format_label else option['label']

                context['data'].append({
                    'value': str(option['value']),
                    'label': label,
                    'query': unicodedata.normalize('NFD', label).encode('ascii', 'ignore').decode('ascii').lower()
                })

        context['widget']['type'] = 'hidden'
        context['widget']['value'] = str(value) if value else ''
        context['widget']['attrs']['id'] += '_hidden'

        return context
