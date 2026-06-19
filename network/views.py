from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.core.paginator import Paginator
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import User, Post, Follow


def index(request):
    # 1. Handle New Post (POST request)
    if request.method == "POST":
        if request.user.is_authenticated:
            content = request.POST.get("content")
            if content:
                Post.objects.create(user=request.user, content=content)
                return HttpResponseRedirect(reverse("index"))

    # 2. Fetch all posts for display
    posts_all = Post.objects.all().order_by("-timestamp")

    # 3. Setup Pagination (10 posts per page)
    paginator = Paginator(posts_all, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # 4. Pass 'page_obj' to the template instead of 'posts_all'
    return render(request, "network/index.html", {
        "posts": page_obj
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

def profile(request, user_id):
    # 1. Get the user whose profile we are viewing
    profile_user = get_object_or_404(User, pk=user_id)
    
    # 2. Get their posts
    user_posts = Post.objects.filter(user=profile_user).order_by("-timestamp")
    
    # 3. Get follower/following counts
    followers = Follow.objects.filter(followed_user=profile_user).count()
    following = Follow.objects.filter(user=profile_user).count()
    
    # 4. Check if current user is following this person
    is_following = False
    if request.user.is_authenticated:
        if Follow.objects.filter(user=request.user, followed_user=profile_user).exists():
            is_following = True

    return render(request, "network/profile.html", {
        "profile_user": profile_user,
        "posts": user_posts,
        "followers_count": followers,
        "following_count": following,
        "is_following": is_following
    })

def toggle_follow(request, user_id):
    if request.method == "POST" and request.user.is_authenticated:
        target_user = get_object_or_404(User, pk=user_id)
        
        # Don't let users follow themselves
        if request.user != target_user:
            follow_rel = Follow.objects.filter(user=request.user, followed_user=target_user)
            
            if follow_rel.exists():
                follow_rel.delete() # Unfollow
            else:
                Follow.objects.create(user=request.user, followed_user=target_user) # Follow
                
        return HttpResponseRedirect(reverse("profile", args=[user_id]))

def following(request):
    # 1. Security: Only signed-in users
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("index"))

    # 2. Get the list of users the current user follows
    # We use .values_list to get just the IDs of those followed users
    followed_users = Follow.objects.filter(user=request.user).values_list("followed_user", flat=True)

    # 3. Filter posts where the author is in that list
    posts = Post.objects.filter(user__in=followed_users).order_by("-timestamp")

    return render(request, "network/following.html", {
        "posts": posts
    })

@csrf_exempt # For simplicity during development, though usually we'd handle CSRF in JS
def edit_post(request, post_id):
    if request.method == "PUT":
        data = json.loads(request.body)
        new_content = data.get("content")
        
        post = Post.objects.get(pk=post_id)
        
        # Security check: Only the author can edit
        if post.user == request.user:
            post.content = new_content
            post.save()
            return JsonResponse({"message": "Post updated successfully."}, status=201)
            
    return JsonResponse({"error": "Invalid request."}, status=400)

@csrf_exempt
def toggle_like(request, post_id):
    if request.method == "POST" and request.user.is_authenticated:
        post = get_object_or_404(Post, pk=post_id)
        user = request.user
        
        # Check if user already liked it
        if post.likes.filter(id=user.id).exists():
            post.likes.remove(user)
            liked = False
        else:
            post.likes.add(user)
            liked = True
            
        return JsonResponse({
            "liked": liked,
            "count": post.likes.count()
        })
    return JsonResponse({"error": "Invalid request"}, status=400)