from django import template
from django.core.exceptions import ObjectDoesNotExist

register = template.Library()


@register.simple_tag(takes_context=True)
def get_provider_app_name(context, provider):
    try:
        return provider.app.name
    except ObjectDoesNotExist:
        return provider.name
