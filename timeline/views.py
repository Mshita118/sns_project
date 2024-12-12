from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Post
from .forms import PostForm


@login_required
def timeline(request):
    posts = Post.objects.all().order_by('-created_at')
    form = PostForm()
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('timeline')
    return render(request, 'timeline/timeline.html', {'posts': posts, 'form': form})
