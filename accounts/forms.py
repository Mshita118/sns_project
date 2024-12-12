from allauth.account.forms import SignupForm
from django import forms
from django.contrib.auth.models import User


class CustomSignupForm(SignupForm):
    full_name = forms.CharField(max_length=50, label="FullName")

    def save(self, request):
        user = super().save(request)
        user.full_name = self.cleaned_data['full_name']
        user.save()
        return user
