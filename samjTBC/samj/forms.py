from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import GlobalSettings
from .models import User


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    number = forms.CharField(max_length=30)

    class Meta:
        model = User
        fields = ("email", "username", "first_name", "last_name", "email", "number", "password1", "password2")

    def save(self, commit=True):
        user = super(CustomUserCreationForm, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']

        # Create a GlobalSettings object and assign it to the user
        global_settings = GlobalSettings.objects.create()
        user.global_settings = global_settings

        if commit:
            user.save()
        return user

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class UpdateUserForm(forms.ModelForm):
    email = forms.EmailField(max_length=30, required=False)
    fullname = forms.CharField(max_length=30, required=False)
    number = forms.CharField(max_length=30, required=False)
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput, required=False)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput, required=False)

    class Meta:
        model = User
        fields = ("email", "username", "fullname", "number")

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        # Check if password fields are being edited
        if password1 or password2:
            # If so, check if both password fields are filled out
            if not (password1 and password2):
                raise forms.ValidationError("Both password fields must be set.")
            elif password1 != password2:
                raise forms.ValidationError("Passwords don't match")

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get("password1")
        if password:
            user.set_password(password)
        if commit:
            user.save()
        return user

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class GlobalSettingsForm(forms.ModelForm):
    class Meta:
        model = GlobalSettings
        fields = ['timezone', 'language', 'theme', 'notifications']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class GitHubIssueForm(forms.Form):
    title = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        'placeholder': '(optional) Enter the title here'
    }))
    name = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={
        'placeholder': '(optional) Enter your name here'
    }))
    email = forms.EmailField(required=False, widget=forms.EmailInput(attrs={
        'placeholder': '(optional) Enter your email here'
    }))
    telephone = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={
        'placeholder': '(optional) Enter your number here'
    }))
    url = forms.URLField(required=False, widget=forms.TextInput(attrs={
        'placeholder': '(optional) Enter the URL where you encounter the error'
    }))
    short_description = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        'placeholder': '(optional) Please summarize the issue in one sentence'
    }))
    detailed_description = forms.CharField(widget=forms.Textarea)
    steps_to_reproduce = forms.CharField(widget=forms.Textarea(attrs={
        'placeholder': '1. \n2. \n3. \n...'
    }))
    expected_results = forms.CharField(widget=forms.Textarea)
    actual_results = forms.CharField(widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
