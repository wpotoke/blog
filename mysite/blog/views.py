from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import render, get_object_or_404
from blog.models import Post
from django.core.mail import send_mail
from django.conf import settings
from django.views.decorators.http import require_POST
from blog.forms import CommentForm, EmailForm



@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Post,
                                id=post_id,
                                status=Post.Status.PUBLISHED)
    comment = None
    form = CommentForm(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
    data = {"post": post, "form": form, "comment": comment}

    return render(request, "blog/post/comment.html", context=data)


def post_share(request, post_id):
    post = get_object_or_404(Post,
                                id=post_id,
                                status=Post.Status.PUBLISHED)
    sent = False
    if request.method == "POST":
        form = EmailForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(
                post.get_absolute_url()
            )
            subject = f"{cd['name']} recomends you read " \
                           f"{post.title}"
            message= f"Read {post.title} at {post_url}\n\n" \
                          f"{cd['name']}\'s ({cd['email']}) comments: {cd['comments']}"
            send_mail(subject, message, settings.EMAIL_HOST_USER, 
                      [cd['to']])
            sent = True
    else:
        form = EmailForm()
    
    data = {"post": post, "form": form, 'sent': sent}

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
    comments = post.comments.filter(active=True)
    form = CommentForm()
    data = {"post": post, "comments": comments, "form": form}

    return render(request, "blog/post/detail.html", context=data)
