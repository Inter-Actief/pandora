from datetime import date, datetime, timedelta, time

from django import forms
from django.db import transaction
from django.forms.models import ModelForm
from django.http import HttpRequest

from pandora.editions.models import Edition, EditionSetting, Day, Event, CommitteeMember
from pandora.pregames.models import Pregame


DEFAULT_DAY_COUNT = 4


class EditionCreateForm(ModelForm):

    class Meta:
        model = Edition
        fields = ('year', 'name')

    start = forms.DateField()
    pregame_start = forms.DateField()

    request: HttpRequest

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super().__init__(*args, **kwargs)

    @transaction.atomic
    def save(self, *args, **kwargs):
        instance: Edition = super().save(*args, **kwargs)

        # Generate settings from defaults
        default_settings = EditionSetting.objects.filter(edition__isnull=True).all()
        for default_setting in default_settings:
            setting = EditionSetting(key=default_setting.key, value=default_setting.value, edition=instance)
            setting.save()

        # Determine start
        start_date: date = self.cleaned_data.get('start')
        current = datetime.combine(start_date, time(20, 0, 0))

        # Determine hype drink and pregame start
        hype_drink_start = datetime.combine(self.cleaned_data.get('pregame_start'), time(hour=16, minute=0, second=0, microsecond=0))
        pregame_start = datetime.combine(self.cleaned_data.get('pregame_start'), time(hour=19, minute=0, second=0, microsecond=0))

        # Generate hype drink event
        event_hype_drink = Event(name='Hype Drink', start=hype_drink_start, end=pregame_start, edition=instance)
        event_hype_drink.save()

        # Generate pregame event
        event_pregame = Event(name='Pregame', start=pregame_start, end=current - timedelta(hours=1), edition=instance)
        event_pregame.save()

        # Generate pregame
        pregame = Pregame(start=pregame_start, end=current - timedelta(hours=1), bonus_amount=10, bonus_reason='Solved pregame', edition=instance)
        pregame.save()

        # Generate days and meeting event
        for number in range(1, DEFAULT_DAY_COUNT + 1):
            start = current
            current += timedelta(hours=20) if number == DEFAULT_DAY_COUNT else timedelta(days=1)

            day = Day(number=number, start=start, end=current, edition=instance)
            day.save()

            event_meeting = Event(name=f'Meeting {number}', start=start - timedelta(hours=1), end=start, edition=instance)
            event_meeting.save()

        # Generate closing drink event
        event_drink = Event(name='Closing drink', start=current, end=current + timedelta(hours=6), edition=instance)
        event_drink.save()

        # Add current user as committee member
        committee_member = CommitteeMember(name=self.request.user.get_full_name(), function='Website', sort_index=1, user=self.request.user, edition=instance)
        committee_member.save()

        return instance
