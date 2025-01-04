from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db import transaction
from django.forms import ModelForm, HiddenInput

from pandora.editions.models import ScoreModification


class ScoreModificationCreateForm(ModelForm):
    class Meta:
        model = ScoreModification
        fields = ('type', 'amount', 'reason', 'team', 'team_member')
        widgets = {
            'team': HiddenInput()
        }

    @transaction.atomic
    def save(self, *args, **kwargs):
        instance = super().save(*args, **kwargs)

        receiver = f'{instance.team_member.name} ({instance.team.name})' if instance.team_member else instance.team.name

        # Send message to feed channels
        async_to_sync(get_channel_layer().group_send)(instance.team.edition.get_feed_channel_group(), {
            'type': 'modification',
            'timestamp': instance.created_at.isoformat(),
            'message': f'{receiver} received {instance.amount} {instance.get_type_display().lower()} points for "{instance.reason}".',
            'modification': {
                'team': {
                    'id': str(instance.team.id),
                    'name': instance.team.name
                }
            }
        })

        return instance


class ScoreModificationUpdateForm(ModelForm):
    class Meta:
        model = ScoreModification
        fields = ('type', 'amount', 'reason', 'team_member')
