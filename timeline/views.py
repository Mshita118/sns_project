from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Post, Follow, Comment, Like, Profile
from .forms import PostForm, CommentForm, ProfileUpdateForm
from allauth.account.views import LoginView


class CustomLoginView(LoginView):
    def form_valid(self, form):
        response = super().form_valid(form)
        if not hasattr(self.request.user, 'profile'):
            Profile.objects.get_or_create(user=self.request.user)
        return response


# プロフィール
@login_required
def profile_view(request, username):
    user = get_object_or_404(User, username=username)
    profile, created = Profile.objects.get_or_create(user=user)
    print(f"User: {user}, Profile created: {created}")
    is_following = Follow.objects.filter(
        follower=request.user, followed=user).exists()
    followers = user.followers.all()
    following = user.following.all()
    return render(request, 'timeline/profile.html', {'profile': profile,
                                                     'is_following': is_following,
                                                     'followers': followers,
                                                     'following': following,
                                                     })


@login_required
def edit_profile(request):
    print("Accessing edit_profile view")
    profile, created = Profile.objects.get_or_create(user=request.user)
    print(f"Profile created: {created}")

    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile', username=request.user.username)
    else:
        form = ProfileUpdateForm(instance=profile)
    return render(request, 'timeline/edit_profile.html', {'form': form})


# タイムライン
@login_required
def timeline(request):
    posts = Post.objects.all().order_by('-created_at')
    posts_with_follow_status = []
    for post in posts:
        is_following = post.user.followers.filter(
            follower=request.user).exists()
        is_liked = post.likes.filter(user=request.user).exists()
        posts_with_follow_status.append({
            'post': post,
            'is_following': is_following,
            'is_liked': is_liked,
        })

    form = PostForm()
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('timeline')

    return render(request, 'timeline/timeline.html', {'posts': posts, 'form': form, 'posts_with_follow_status': posts_with_follow_status, })

# 投稿編集機能


@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, user=request.user)
    if request.method == "POST":
        post.delete()
        messages.success(request, "投稿を削除しました。")
        return redirect('timeline')
    return render(request, 'timeline/confirm_post.html', {'post': post})


@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, user=request.user)
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_detail', post_id=post.id)
    else:
        form = PostForm(instance=post)
    return render(request, 'timeline/edit_post.html', {'form': form, 'post': post})

# 投稿削除機能


# フォロー機能
@login_required
def follow_user(request, user_id):
    followed_user = User.objects.get(id=user_id)

    if not Follow.objects.filter(follower=request.user, followed=followed_user).exists():
        Follow.objects.create(follower=request.user, followed=followed_user)

    return redirect('timeline')


@login_required
def unfollow_user(request, user_id):
    followed_user = User.objects.get(id=user_id)

    follow = Follow.objects.filter(
        follower=request.user, followed=followed_user)
    follow = Follow.objects.filter(
        follower=request.user, followed=followed_user)
    if follow.exists():
        follow.delete()

    return redirect('timeline')


def search_posts(request):
    query = request.GET.get('q')
    if query:
        posts = Post.objects.filter(content__icontains=query)
        users = User.objects.filter(username__icontains=query)
    else:
        posts = []
        users = []
    return render(request, 'timeline/search_results.html', {
        'query': query,
        'posts': posts,
        'users': users,
    })


@login_required
def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.all()
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()
            return redirect('post_detail', post_id=post.id)
    else:
        form = CommentForm()
    return render(request, 'timeline/post_detail.html', {
        'post': post,
        'comments': comments,
        'form': form
    })


# いいね
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    like, created = Like.objects.get_or_create(user=request.user, post=post)
    if not created:
        like.delete()
    return redirect('post_detail', post_id=post.id)


def follower_list(request, username):
    user = get_object_or_404(User, username=username)
    followers = Follow.objects.filter(followed=user)
    return render(request, 'timeline/follower_list.html', {'user': user, 'followers': followers})


def following_list(request, username):
    user = get_object_or_404(User, username=username)
    following = Follow.objects.filter(follower=user)
    return render(request, 'timeline/following_list.html', {'user': user, 'following': following})
