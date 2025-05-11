from django.http import Http404
from django.shortcuts import render
from blog.models import Post


def post_list(request):

    posts = Post.published.all()

    data = {"posts": posts}
    return render(request, "blog/post/list.html", data)


def post_detail(request, id):
    try:
        post = Post.published.get(id=id)
        data = {"post": post}

    except Post.DoesNotExist:
        raise Http404("No post found.")

    return render(request, "blog/post/detail.html", context=data)
