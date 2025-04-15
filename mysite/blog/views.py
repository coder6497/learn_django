from django.shortcuts import render
from .models import Post
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

