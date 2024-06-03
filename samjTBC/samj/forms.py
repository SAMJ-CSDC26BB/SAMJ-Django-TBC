from django import forms
from .models import GlobalSettings, CallForwardingRecords, TbcDestination


class GlobalSettingsForm(forms.ModelForm):
    class Meta:
        model = GlobalSettings
        fields = ['timezone', 'language', 'theme', 'notifications']


from .models import CallForwardingRecords, TbcDestination

class CallForwardingRecordsForm(forms.ModelForm):
    class Meta:
        model = CallForwardingRecords
        fields = ['kopfnummer', 'anfang', 'ende', 'dauer', 'erinnerung', 'durchwahl', 'ziel']

class TbcDestinationForm(forms.ModelForm):
    class Meta:
        model = TbcDestination
        fields = ['name', 'value', 'type']