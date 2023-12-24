from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean_username(self):
        data = self.cleaned_data.get('username')
        if not User.objects.filter(username__exact=data).exists():
            raise ValidationError("User doesn't exist")
        return data

