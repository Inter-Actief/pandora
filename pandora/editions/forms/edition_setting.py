from django.forms import ModelForm, HiddenInput

from pandora.editions.models import EditionSetting


class EditionSettingModelForm(ModelForm):

    class Meta:
        model = EditionSetting
        fields = ('edition', 'key', 'value')
        widgets = {
            'edition': HiddenInput()
        }
