from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Post
from .models import Follow
from .forms import PostForm

#タイムライン
@login_required
def timeline(request):
    posts = Post.objects.all().order_by('-created_at')
    posts_with_follow_status =[]
    for post in posts:
        is_following = post.user.followers.filter(follower=request.user).exists()
        posts_with_follow_status.append({
            'post': post,
            'is_following': is_following,
        })
    form = PostForm()
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('timeline')
    return render(request, 'timeline/timeline.html', {'posts': posts, 'form': form})

#フォロー機能
@login_required

def follow_user(request, user_id):
    followed_user = User.objects.get(id=user_id)

    if not Follow.objects.filter(followe=request.user, followed=followed_user).exists():
        Follow.objects.create(follower=request.user, followed=followed_user)

    return redirect('timeline')

@login_required
def unfollow_user(request, user_id):
    followed_user = User.ubjects.get(id=user_id)

    follow = Follow.objects.filter(follower=request.user, followed=followed_user)
    if follow.exists():
        follow.delete()

    return redirect('timeline')
