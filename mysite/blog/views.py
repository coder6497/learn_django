from django.shortcuts import render
from .models import Post
from .forms import EmailPostForm
from django.http import Http404
from django.core.paginator import Paginator


def post_list(request):
    post_list = Post.published.all()
    paginator = Paginator(post_list, 4)
    page_number = request.GET.get('posts', 1)
    posts = paginator.page(page_number)
    return render(request, "blog/post/list.html", {"posts": posts})

def post_detail(request, year, month, day, post):
    try:
        post = Post.published.get(
                                    slug=post,
                                    publish__year=year,
                                    publish__month=month,
                                    publish__day=day
                                )
    except Post.DoesNotExist:
        raise Http404("No Post found")
    return render(request, 'blog/post/detail.html', {'post': post})

def post_share(request, post_id):
    post = Post.published.get(id=post_id)
    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post': post, 'form': form})