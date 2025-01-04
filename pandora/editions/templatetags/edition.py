from django import template
from django.core.exceptions import ObjectDoesNotExist

from pandora.editions.models import Edition

register = template.Library()


@register.simple_tag(takes_context=True)
def current_edition(context):
    try:
        return context['edition'] if 'edition' in context and context['edition'] else Edition.get_latest()
    except ObjectDoesNotExist:
        return None


@register.simple_tag
def latest_edition():
    try:
        return Edition.get_latest()
    except ObjectDoesNotExist:
        return None


@register.simple_tag(takes_context=True)
def current_edition_year(context):
    try:
        edition = context['edition'] if 'edition' in context and context['edition'] else Edition.get_latest()
        return edition.year
    except ObjectDoesNotExist:
        return ''


@register.simple_tag
def latest_edition_year():
    try:
        edition = Edition.get_latest()
        return edition.year
    except ObjectDoesNotExist:
        return None


@register.simple_tag(takes_context=True)
def current_committee_member(context):
    if not context['request'].user.is_authenticated:
        return None

    try:
        edition = context['edition'] if 'edition' in context and context['edition'] else Edition.get_latest()

        return context['request'].user.committee_memberships.filter(edition=edition).first()
    except ObjectDoesNotExist:
        return None


@register.simple_tag
def edition_years():
    return Edition.objects.order_by('-year').values_list('year', flat=True)
