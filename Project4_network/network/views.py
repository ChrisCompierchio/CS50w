from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse
from django.core.paginator import Paginator

from .models import User, Post, Like, Follow


def index(request):
    if request.method == "POST":
        text = request.POST.get("post-text")
        author = User.objects.get(pk=request.user.id)
        if text == None:
            pass
        else:
            new_post = Post(author=author, text=text)
            new_post.save()

        likes = Like.objects.all()
        likedPosts = []
        for like in likes:
            if like.liker.id == request.user.id:
                likedPosts.append(like.liked_post.id)
        posts = Post.objects.all().order_by("id").reverse()

        paginator = Paginator(posts, 10)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        return HttpResponseRedirect(reverse(index), {
            "page_obj": page_obj,
            "posts": posts,
            "likedPosts": likedPosts
        })
    else:
        likes = Like.objects.all()
        likedPosts = []
        for like in likes:
            if like.liker.id == request.user.id:
                likedPosts.append(like.liked_post.id)
        posts = Post.objects.all().order_by("id").reverse()

        paginator = Paginator(posts, 10)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        return render(request, "network/index.html", {
            "page_obj": page_obj,
            "posts": posts,
            "likedPosts": likedPosts
        })


def login_view(request):
    if request.method == "POST":

        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

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

        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

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

def newLike(request, post_id):

    new_like = Like(liked_post = Post.objects.get(pk=post_id), liker = request.user)
    new_like.save()

    return HttpResponseRedirect(reverse(index))

def unlike(request, post_id):
    new_like = Like.objects.get(liked_post = Post.objects.get(pk=post_id), liker = request.user)
    new_like.delete()

    return HttpResponseRedirect(reverse(index))

def profile(request, clickedUser):
    if request.method == "POST" or request.method == "GET":
        usersPosts = []
        everyPost = Post.objects.all().order_by("id").reverse()
        for post in everyPost:
            if post.author.username == clickedUser:
                usersPosts.append(post)
        totalFollows = Follow.objects.all()
        usersFollowers = []
        usersFollows = []

        for follow in totalFollows:
            if (follow.followee.username == clickedUser):
                usersFollowers.append(follow)
            elif (follow.follower.username == clickedUser):
                usersFollows.append(follow)

        numFollowers = len(usersFollowers)
        numFollows = len(usersFollows)

        likes = Like.objects.all()
        likedPosts = []
        for like in likes:
            if like.liker.id == request.user.id:
                likedPosts.append(like.liked_post.id)

        ownPage = False
        if clickedUser == request.user.username:
            ownPage = True

        clicked = User.objects.get(username=clickedUser)
        clickedUserId = clicked.id

        alreadyFollowing = False
        for follow in usersFollowers:
            if request.user.id == follow.follower.id:
                alreadyFollowing = True
                break

        paginator = Paginator(usersPosts, 10)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        return render(request, "network/profile.html", {
            "page_obj": page_obj,
            "usersFollowers": usersFollowers,
            "usersFollows": usersFollows,
            "usersPosts": usersPosts,
            "numFollowers": numFollowers,
            "numFollows": numFollows,
            "likedPosts": likedPosts,
            "ownPage": ownPage,
            "alreadyFollowing": alreadyFollowing,
            "clickedUser": clickedUser,
            "clickedUserId": clickedUserId
        })

def newFollow(request, clickedUserId):
    follower = User.objects.get(pk=request.user.id)
    followee = User.objects.get(pk=clickedUserId)

    newFollow = Follow(follower=follower, followee=followee)
    newFollow.save()

    return HttpResponseRedirect(reverse(index))


def deleteFollow(request, clickedUserId):
    unfollower = User.objects.get(pk=request.user.id)
    unfollowee = User.objects.get(pk=clickedUserId)

    newUnfollow = Follow.objects.get(follower=unfollower, followee=unfollowee)
    newUnfollow.delete()

    return HttpResponseRedirect(reverse(index))

def following(request):
    if request.method == "POST" or request.method == "GET":
        follows = Follow.objects.all()
        followees = []
        allPosts = Post.objects.all().order_by("id").reverse()
        followeesPosts = []
        for follow in follows:
            if follow.follower.id == request.user.id:
                followees.append(follow.followee)
        for post in allPosts:
            if post.author in followees:
                followeesPosts.append(post)

        likes = Like.objects.all()
        likedPosts = []
        for like in likes:
            if like.liker.id == request.user.id:
                likedPosts.append(like.liked_post.id)

        paginator = Paginator(followeesPosts, 10)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        return render(request, "network/following.html", {
            "page_obj": page_obj,
            "likedPosts": likedPosts,
            "followeesPosts": followeesPosts
        })

@csrf_exempt
def post(request, post_id):

    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)

    if request.method == "GET":
        return JsonResponse(post.serialize())

    elif request.method == "PUT":
        data = json.loads(request.body)
        if data.get("text") is not None:
            post.text = data["text"]
        if data.get("likes") is not None:
            post.likes = data["likes"]
        post.save()
        return HttpResponse(status=204)

    else:
        return JsonResponse({
            "error": "GET or PUT request required."
        }, status=400)


@csrf_exempt
def like(request):

    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    data = json.loads(request.body)

    post_liker = data.get("liker")
    post_id = data.get("liked_post")

    new_like = Like(liker=post_liker, liked_post=Post.objects.get(pk=post_id))
    new_like.save()

    return JsonResponse({"message": "Email sent successfully."}, status=201)




