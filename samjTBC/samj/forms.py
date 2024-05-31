# samj/forms.py

from django import forms
from .models import Kopfnummer, Zielnummer

class EntryForm(forms.Form):
    kopfnummer = forms.ModelChoiceField(queryset=Kopfnummer.objects.none())
    durchwahl = forms.CharField(required=False)
    zielnummer = forms.ModelChoiceField(queryset=Zielnummer.objects.none())
    anfangsdatum = forms.DateTimeField(widget=forms.TextInput(attrs={'type': 'datetime-local'}))
    endedatum = forms.DateTimeField(widget=forms.TextInput(attrs={'type': 'datetime-local'}))

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(EntryForm, self).__init__(*args, **kwargs)
        self.fields['kopfnummer'].queryset = Kopfnummer.objects.filter(user=user)
        self.fields['zielnummer'].queryset = Zielnummer.objects.filter(user=user)
