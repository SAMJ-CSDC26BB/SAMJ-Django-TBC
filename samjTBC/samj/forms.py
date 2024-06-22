from django import forms

from .models import GlobalSettings


class GlobalSettingsForm(forms.ModelForm):
    class Meta:
        model = GlobalSettings
        fields = ['timezone', 'language', 'theme', 'notifications']


class GitHubIssueForm(forms.Form):
    title = forms.CharField(max_length=100)
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    telephone = forms.CharField(max_length=100)
    url = forms.URLField()
    short_description = forms.CharField(max_length=100)
    detailed_description = forms.CharField(widget=forms.Textarea)
    steps_to_reproduce = forms.CharField(widget=forms.Textarea)
    expected_results = forms.CharField(widget=forms.Textarea)
    actual_results = forms.CharField(widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
