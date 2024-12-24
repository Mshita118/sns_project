from django.shortcuts import render
from allauth.account.views import LoginView
from timeline.models import Profile
from .forms import CustomLoginForm


class CustomLoginView(LoginView):
    form_class = CustomLoginForm

    def form_valid(self, form):
        user = form.get_user()
        print(f"User: {user}")
        profile, created = Profile.objects.get_or_create(user=user)
        print(f"Profile created: {created}")
        if created:
            profile.user = user
            profile.save()
        return super().form_valid(form)
