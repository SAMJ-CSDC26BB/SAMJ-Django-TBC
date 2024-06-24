from django import forms
from .models import GlobalSettings
from .models import CallForwarding

class GlobalSettingsForm(forms.ModelForm):
    class Meta:
        model = GlobalSettings
        fields = ['timezone', 'language', 'theme', 'notifications']

class CallForwardingForm(forms.ModelForm):
    class Meta:
        model = CallForwarding
        fields = ['calledNumber', 'destination', 'startDate', 'endDate']