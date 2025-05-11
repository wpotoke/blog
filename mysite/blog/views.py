from django.core.paginator import EmptyPage, Paginator
from django.http import Http404
from django.shortcuts import render, get_object_or_404
from blog.models import Post


def post_list(request):

    post_list = Post.published.all()

    paginator = Paginator(post_list, 3)
    page_number = request.GET.get('page', 1)
    try:
        posts = paginator.page(page_number)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

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
