from django import template
from django.core.exceptions import ObjectDoesNotExist

from pandora.editions.models import Edition

register = template.Library()


@register.simple_tag(takes_context=True)
def current_team(context):
    if not context['request'].user.is_authenticated:
        return None

    try:
        edition = Edition.get_latest()

        return edition.teams.filter(members__user=context['request'].user).first()
    except ObjectDoesNotExist:
        return None


@register.simple_tag(takes_context=True)
def current_team_member(context):
    if not context['request'].user.is_authenticated:
        return None

    try:
        edition = Edition.get_latest()

        return context['request'].user.memberships.filter(team__edition=edition).first()
    except ObjectDoesNotExist:
        return None
