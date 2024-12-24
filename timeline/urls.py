from django.urls import path
from . import views
from accounts.views import CustomLoginView


urlpatterns = [
    path('', views.timeline, name='timeline'),
    path('follow/<int:user_id>/', views.follow_user, name='follow_user'),
    path('unfollow/<int:user_id>/', views.unfollow_user, name='unfollow_user'),
    path('search/', views.search_posts, name='search_posts'),
    path('post/<int:post_id>/edit/', views.edit_post, name='edit_post'),
    path('<int:post_id>/', views.post_detail, name='post_detail'),
    path('<int:post_id>/like/', views.like_post, name='like_post'),
    path('post/<int:post_id>/delete/', views.delete_post, name='delete_post'),
    path('profile/<str:username>/', views.profile_view, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('accounts/login/', CustomLoginView.as_view(), name='account_login'),
]
