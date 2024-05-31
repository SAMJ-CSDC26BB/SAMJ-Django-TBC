# samj/forms.py

from django import forms

class EntryForm(forms.Form):
    kopfnummer = forms.ChoiceField(choices=[('4327', '4327'), ('4328', '4328')])
    durchwahl = forms.CharField(required=False)
    zielnummer = forms.ChoiceField(choices=[('Beierl', 'Beierl'), ('Info', 'Info')])
    anfangsdatum = forms.DateTimeField(widget=forms.TextInput(attrs={'type': 'datetime-local'}))
    endedatum = forms.DateTimeField(widget=forms.TextInput(attrs={'type': 'datetime-local'}))
