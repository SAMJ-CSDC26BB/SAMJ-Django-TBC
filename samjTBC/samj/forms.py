from django import forms
from .models import Zielnummer
from django.contrib.auth.models import User

class EntryForm(forms.Form):
    kopfnummer = forms.ChoiceField(choices=[('4327', '4327'), ('4328', '4328')])
    durchwahl = forms.CharField(required=False)
    zielnummer = forms.ChoiceField(choices=[('Beierl', 'Beierl'), ('Info', 'Info')])
    anfangsdatum = forms.DateTimeField(widget=forms.TextInput(attrs={'type': 'datetime-local'}))
    endedatum = forms.DateTimeField(widget=forms.TextInput(attrs={'type': 'datetime-local'}))

class ZielnummerForm(forms.ModelForm):
    user = forms.ModelChoiceField(queryset=User.objects.all(), empty_label="Select User", required=True)

    class Meta:
        model = Zielnummer
        fields = ['user', 'number']