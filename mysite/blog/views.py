from django.shortcuts import render
from .models import Post
from .forms import EmailPostForm, CommentForm
from django.http import Http404
from django.core.paginator import Paginator
from django.core.mail import send_mail
from django.views.decorators.http import require_POST

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
        comments = post.comments.filter(active=True)
        form = CommentForm()
    except Post.DoesNotExist:
        raise Http404("No Post found")
    return render(request, 'blog/post/detail.html', {'post': post, 'comments': comments, "form": form})

def post_share(request, post_id):
    try:
        post = Post.published.get(id=post_id)
        sent = False
        if request.method == 'POST':
            form = EmailPostForm(request.POST)
            if form.is_valid():
                cd = form.cleaned_data
                post_url = request.build_absolute_uri(post.get_absolute_url())
                subject = f"{cd['name']} рекомендует вам прочесть {post.title}"
                message = f"Посмотреть {post.title} по адресу {post_url}\n\nСообщение от {cd['name']}: {cd['comments']}"
                send_mail(subject, message, 'rty.sem@yandex.ru', [cd['to']])
                sent = True
        else:
            form = EmailPostForm()
    except Post.DoesNotExist:
        raise Http404("No Post Found")
    return render(request, 'blog/post/share.html', {'post': post, 'form': form, 'sent': sent})

@require_POST
def post_comment(request, post_id):
    try:
        post = Post.published.get(id=post_id)
        comment = None
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
    except Post.DoesNotExist:
        raise Http404("No Post Found")
    return render(request, 'blog/post/comments.html', {'post': post, 'form': form, 'comment': comment})