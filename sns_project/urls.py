from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('timeline/', include('timeline.urls')),
    path('', lambda request: redirect('timeline')),
]
