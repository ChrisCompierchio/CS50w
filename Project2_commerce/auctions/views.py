from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from auctions.models import User, Listing, Bid, Comment


def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.all()
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
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


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
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


def create(request):
    if request.method == "GET":
        return render(request, "auctions/create.html")
    else:
        title = request.POST["title"]
        description = request.POST["description"]
        starting_bid = request.POST["starting_bid"]
        image_url = request.POST["image_url"]
        category = request.POST["category"]

        new_listing = Listing(title=title, description=description, starting_bid=starting_bid, image=image_url, category=category, user = request.user, active = True)
        new_listing.save()

        return HttpResponseRedirect(reverse("index"))

def listing_page(request, id):
    if request.method == "GET":
        return render(request, "auctions/listing.html")
    else:
        listing = Listing.objects.get(pk=id)
        on_watchlist = False
        message = ""
        win_message = ""
        bid_message = "No Current Bids"
        bid_exists = Bid.objects.all().filter(listing_id = id).exists()
        comment_exists = Comment.objects.all().filter(listing_id = id).exists()
        comments = None
        close = False
        if bid_exists:
            bid_message = f'Current Bid: ${Bid.objects.all().filter(listing_id = id).last().value} by {Bid.objects.all().filter(listing_id = id).last().user}'
        if request.user in listing.watchlist.all():
            message = "This is in your watchlist!"
            on_watchlist = True
        else:
            message = "This is not in your watchlist!"
            on_watchlist = False
        if (listing.active == False) and (Bid.objects.all().filter(listing_id = id).last().user == request.user.username):
            win_message = "You Have Won This Item!!!"
        if request.user.username == listing.user:
            close = True
        if comment_exists:
            comments = Comment.objects.all().filter(listing_id = id)
        if request.POST.get("add") == "Add To Watchlist":
            message = "This is in your watchlist!"
            on_watchlist = True
            listing.watchlist.add(request.user)
        elif request.POST.get("add") == "Remove From Watchlist":
            message = "This is not in your watchlist!"
            on_watchlist = False
            listing.watchlist.remove(request.user)
        elif request.POST.get("place_bid"):
            if (request.POST.get("bid") == None) or (request.POST.get("bid") == "") or (float(request.POST.get("bid")) == listing.starting_bid):
                bid_message = "Please Enter Valid Bid"
            else:
                bid_exists = Bid.objects.all().filter(listing_id = id).exists()
                if bid_exists:
                    last_bid = Bid.objects.all().filter(listing_id = id).last().value
                    if(last_bid >= float(request.POST.get("bid"))):
                        bid_message = "Please Enter a Bid Greater Than the Current Bid"
                    else:
                        new_bid = '{:20,.2f}'.format(float(request.POST.get("bid")))
                        new_bid = "$".strip() + new_bid.strip()
                        bid_message = f'Current Bid: {new_bid} by {request.user}'

                        updated_bid = Bid(user = request.user, value = float(request.POST.get("bid")), listing=listing)
                        updated_bid.save()
                else:
                    new_bid = '{:20,.2f}'.format(float(request.POST.get("bid")))
                    new_bid = "$".strip() + new_bid.strip()
                    bid_message = f'Current Bid: {new_bid} by {request.user}'

                    updated_bid = Bid(user = request.user, value = float(request.POST.get("bid")), listing = listing)
                    updated_bid.save()
        elif request.POST.get("close"):
            listing.active = False
            listing.save()
            win_message = "You Have Won This Item!!!"
        elif request.POST.get("comment"):
            name = request.user
            comment = request.POST["comment"]

            if comment == "":
                return render(request, "auctions/listing.html")
            else:
                new_comment = Comment(user = name, text = comment, listing = listing)
                new_comment.save()
                comments = Comment.objects.all().filter(listing_id = id)

        return render(request, "auctions/listing.html", {
            "listing": listing,
            "on_watchlist": on_watchlist,
            "wl_message": message,
            "bid_message": bid_message,
            "close": close,
            "win_message": win_message,
            "comments": comments
        })


def watchlist(request):
    return render(request, "auctions/watchlist.html", {
        "listings": Listing.objects.all().filter(watchlist = request.user, active = True)
    })

def categories(request):
    return render(request, "auctions/categories.html")

def category(request):
    if request.method == "GET":
        return render(request, "auctions/categories.html")
    else:
        if request.POST.get("fashion"):
            cat = "Fashion"
        elif request.POST.get("home"):
            cat = "Home"
        elif request.POST.get("electronics"):
            cat = "Electronics"
        else:
            cat = "Clothing"


        return render(request, "auctions/category.html", {
            "listings": Listing.objects.all().filter(category = cat, active = True),
            "category": cat
            })


