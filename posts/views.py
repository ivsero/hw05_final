from django.shortcuts import redirect, get_object_or_404, render
from .models import Post, Group, Comment, Follow
from .forms import PostForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from django.http import HttpResponseForbidden, HttpResponseNotAllowed

USER = get_user_model()


def index(request):
    """Page renderer function for posts"""

    post_list = Post.objects.all().order_by('-pub_date')
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'index.html', {
        'page': page,
    })


def group_posts(request, slug):
    """Page renderer function for community"""

    group = get_object_or_404(Group, slug=slug)
    post_list = group.posts.all()
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    return render(request, 'group.html', {
        'group': group,
        'page': page,
    })


@login_required
def new_post(request):
    """New post renderer function for users"""

    form = PostForm()
    if request.method == 'POST':
        form = PostForm(
            request.POST,
            files=request.FILES or None,
        )
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.author = request.user
            new_post.save()
            return redirect('index')
    return render(request, 'post_form.html', {'form': form})


def profile(request, username):
    """Profile renderer function for users"""

    user_profile = get_object_or_404(USER, username=username)
    post_list = Post.objects.filter(
        author=user_profile
    ).order_by('-pub_date')
    posts_count = post_list.count()
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    followers = Follow.objects.filter(author=user_profile.id).count()
    follows = Follow.objects.filter(user=user_profile.id).count()
    following = Follow.objects.filter(
        user=request.user.id, author=user_profile.id).exists()

    return render(request, 'profile.html', {
        'user_profile': user_profile,
        'page': page,
        'posts_count': posts_count,
        'followers': followers,
        'follows': follows,
        'following': following
    })


def post_view(request, username, post_id):
    """Post view renderer function for users"""

    user_profile = get_object_or_404(USER, username=username)
    post = get_object_or_404(Post, pk=post_id, author=user_profile)
    post_list = Post.objects.filter(
        author=user_profile
    ).order_by('-pub_date')
    posts_count = post_list.count()
    form = CommentForm()
    comment_list = Comment.objects.filter(
        post=post
    ).order_by('-created')
    followers = Follow.objects.filter(author=user_profile.id).count()
    follows = Follow.objects.filter(user=user_profile.id).count()
    following = Follow.objects.filter(
        user=request.user.id, author=user_profile.id).all()
    return render(request, 'post.html', {
        'user_profile': user_profile,
        'post': post,
        'posts_count': posts_count,
        'comment_list': comment_list,
        'form': form,
        'followers': followers,
        'follows': follows,
        'following': following
    })


def post_edit(request, username, post_id):
    """Post edit renderer function for users"""

    user = get_object_or_404(USER, username=username)
    post = get_object_or_404(Post, id=post_id, author=user)

    if request.user != user:
        return redirect(
            'post',
            username=user.username,
            post_id=post_id
        )

    form = PostForm(
        request.POST or None,
        files=request.FILES or None,
        instance=post
    )

    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect(
            'post',
            username=request.user.username,
            post_id=post_id
        )

    return render(request, 'post_form.html', {
        'form': form,
        'post': post
    })


@login_required
def add_comment(request, username, post_id):
    post = get_object_or_404(Post, pk=post_id)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.author = request.user
            new_comment.post = post
            new_comment.save()
            return redirect(
                'post',
                username=post.author.username,
                post_id=post_id
            )
        return render(request, 'comments.html', {
            'post': post,
            'form': form
        })
    return HttpResponseNotAllowed('Error 405: Method Not Allowed')


@login_required
def follow_index(request):
    post_list = Post.objects.filter(author__following__user=request.user).all().order_by('-pub_date')
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'follow.html', {
        'page': page,
        'paginator': paginator
    })


@login_required
def profile_follow(request, username):
    user = request.user
    user_profile = get_object_or_404(USER, username=username)

    if user_profile.id != user.id:
        Follow.objects.get_or_create(user=request.user, author=user_profile)
    else:
        return HttpResponseForbidden()
    return redirect(
        'profile',
        username=username
    )


@login_required
def profile_unfollow(request, username):
    user_profile = get_object_or_404(USER, username=username)
    Follow.objects.filter(
        user=request.user,
        author=user_profile
    ).delete()
    return redirect(
        'profile',
        username=username
    )


def page_not_found(request, exception):
    return render(
        request,
        "misc/404.html",
        {"path": request.path},
        status=404
    )


def server_error(request):
    return render(request, "misc/500.html", status=500)
