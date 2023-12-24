from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

from app.models import Profile, Question, Tag


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean_username(self):
        data = self.cleaned_data.get('username')
        if not User.objects.filter(username__exact=data).exists():
            raise ValidationError("User doesn't exist")
        return data


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_again = forms.CharField(label='Repeat password, please', widget=forms.PasswordInput)
    nickname = forms.CharField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean(self):
        password1 = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password_again')

        if password1 != password2:
            raise ValidationError({'password': 'Passwords do not match', 'password_again': 'Passwords do not match', })

        username = self.cleaned_data.get('username')
        if User.objects.filter(username__exact=username).exists():
            raise ValidationError({'username': 'User already exists'})

    def save(self, **kwargs):
        self.cleaned_data.pop('password_again')
        nickname = self.cleaned_data.pop('nickname')
        u = User.objects.create_user(**self.cleaned_data)
        u.save()
        p = Profile(user=u, nickname=nickname)
        p.save()
        return u


class QuestionFrom(forms.ModelForm):
    title = forms.CharField(min_length=5, required=True)
    text = forms.CharField(min_length=10, required=True, widget=forms.Textarea)

    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Question
        fields = ['title', 'text', 'tags']
