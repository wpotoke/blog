from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import render, get_object_or_404
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank, TrigramSimilarity
from django.db.models import Count
from blog.models import Post
from taggit.models import Tag
from django.core.mail import send_mail
from django.conf import settings
from django.views.decorators.http import require_POST
from blog.forms import CommentForm, EmailForm, SearchForm



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


def post_list(request, tag_slug=None):

    post_list = Post.published.all()

    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        post_list = Post.objects.filter(tags__in=[tag])

    paginator = Paginator(post_list, 3)
    page_number = request.GET.get('page', 1)
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    data = {"posts": posts, "tag": tag}

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
    
    post_tags_ids = post.tags.values_list("id", flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by("-same_tags", "-publish")[:4]
    
    data = {"post": post, "comments": comments, "form": form, "similar_posts": similar_posts}

    return render(request, "blog/post/detail.html", context=data)


def post_search(request):
    form = SearchForm()
    query = None
    res = []

    if "query" in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            res = Post.published.annotate(
                similarity=TrigramSimilarity('title', query)
            ).filter(similarity__gt=0.1).order_by("-similarity")

    data = {"form": form, "query": query, "results": res}

    return render(request, "blog/post/search.html", data)
