from django import template
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag(takes_context=True)
def active(context, url_name, **kwargs):
    if context.request.resolver_match.url_name == url_name:
        for name, value in kwargs.items():
            if context.request.resolver_match.kwargs.get(name, None) != value:
                return ''
        return 'active'
    return ''


@register.simple_tag
def call(value, callable_name: str, *args):
    callable_value = value[callable_name] if type(value) is dict else getattr(value, callable_name)
    return callable_value(*args)


@register.simple_tag
def define(value):
    return value


@register.filter
def colour_first_letter(text: str):
    first, other = text[0], text[1:]
    return mark_safe(f'<span class="first-letter">{conditional_escape(first)}</span>{conditional_escape(other)}')


@register.filter
def map_by_key(values: list, key: str):
    return [value[key] if type(value) is dict else getattr(value, key) for value in values]


@register.filter
def maximum(value, compare_value):
    return max(value, compare_value)


@register.filter
def minimum(value, compare_value):
    return min(value, compare_value)
