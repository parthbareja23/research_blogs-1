from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .models import Post


def post_list(request):

    posts = Post.objects.all().order_by('-created_on')

    return render(
        request,
        'index.html',
        {'posts': posts}
    )


@login_required
def create_post(request):

    error = None

    if request.method == "POST":

        title = request.POST.get("title", "").strip()
        body = request.POST.get("body", "").strip()

        if not title:
            error = "Title required hai."

        elif not body:
            error = "Content required hai."

        else:

            Post.objects.create(
                title=title,
                body=body,
                author=request.user
            )

            return redirect('/')

    return render(
        request,
        'create.html',
        {'error': error}
    )


def user_login(request):

    error = None

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user:
            login(request, user)
            return redirect('/')

        error = "Invalid username or password"

    return render(
        request,
        'login.html',
        {'error': error}
    )


def user_logout(request):

    logout(request)

    return redirect('/login/')