from django.views.generic import ListView, UpdateView

from pandora.editions.forms.edition_setting import EditionSettingModelForm
from pandora.editions.mixins import CommitteeMemberAccessMixin, EditionMixin
from pandora.editions.models import EditionSetting


class EditionSettingListView(EditionMixin, CommitteeMemberAccessMixin, ListView):
    model = EditionSetting
    context_object_name = 'settings'

    def get_queryset(self):
        # Ensure all default settings exist
        for default_setting in EditionSetting.objects.filter(edition__isnull=True).all():
            if not EditionSetting.objects.filter(key=default_setting.key, edition=self.edition).exists():
                setting = EditionSetting(key=default_setting.key, value=default_setting.value, edition=self.edition)
                setting.save()

        return self.edition.settings.order_by('key')


class EditionSettingUpdateView(EditionMixin, CommitteeMemberAccessMixin, UpdateView):
    model = EditionSetting
    form_class = EditionSettingModelForm
    context_object_name = 'setting'
    template_name_suffix = '_update'
