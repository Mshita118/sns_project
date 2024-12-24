from allauth.account.forms import SignupForm, LoginForm
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


class CustomSignupForm(SignupForm):
    full_name = forms.CharField(max_length=50, label="FullName")

    def save(self, request):
        user = super().save(request)
        user.full_name = self.cleaned_data['full_name']
        user.save()
        return user


class CustomLoginForm(LoginForm):
    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise forms.ValidationError(
                "This account is inactive", code='inactive'
            )

    def get_user(self):
        if not hasattr(self, '_user_cache'):
            self._user_cache = authenticate(
                username=self.cleaned_data.get('login'), password=self.cleaned_data.get('password')
            )
            return self._user_cache

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['login'].widget.attrs.update({'class': 'form-control'})
        self.fields['password'].widget.attrs.update({'class': 'form-control'})
