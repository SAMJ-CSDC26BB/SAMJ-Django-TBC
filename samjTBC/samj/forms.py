from django import forms

from .models import GlobalSettings


class GlobalSettingsForm(forms.ModelForm):
    class Meta:
        model = GlobalSettings
        fields = ['timezone', 'language', 'theme', 'notifications']


class GitHubIssueForm(forms.Form):
    title = forms.CharField(max_length=100)
    description = forms.CharField(widget=forms.Textarea)
