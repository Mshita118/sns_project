from django.contrib import admin
from .models import Post, Follow, Comment, Profile


admin.site.register(Post)
admin.site.register(Follow)
admin.site.register(Comment)
admin.site.register(Profile)
