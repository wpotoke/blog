from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import Http404
from django.shortcuts import render, get_object_or_404
from blog.models import Post
from blog.forms import EmailForm

def post_share(request, post_id):
    post = get_object_or_404(Post,
                                id=post_id,
                                status=Post.Status.PUBLISHED)
    if request.method == "POST":
        form = EmailForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
    else:
        form = EmailForm()
    
    data = {"post": post, "form": form}

    return render(request, 'blog/post/share.html', context=data)


def post_list(request):

    post_list = Post.published.all()

    paginator = Paginator(post_list, 3)
    page_number = request.GET.get('page', 1)
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        posts = paginator.page(1)
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
