from django.http import Http404
from django.shortcuts import render, get_object_or_404
from blog.models import Post


def post_list(request):

    posts = Post.published.all()

    data = {"posts": posts}
    return render(request, "blog/post/list.html", data)


def post_detail(request, year, month, day, post):

    post = get_object_or_404(Post, 
                            status=Post.Status.PUBLISHED,
                            slug=post,
                            publish__year=year,
                            publish__month=month,
                            publish__day=day)
    data = {"post": post}

    return render(request, "blog/post/detail.html", context=data)
