from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages
 
from .models import User, Auction, Category, Bid, Comment


def index(request):
    category_query = request.GET.get('category')
    category = Category.objects.get(title__iexact=category_query) if category_query else None

    
    if not category:
        auctions = Auction.objects.all().filter(is_active=True)
    else:
        auctions = Auction.objects.all().filter(is_active=True, category=category)
    
    return render(request, "auctions/index.html",{
        "auctions": auctions
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

def create_auction(request):
    user = request.user
    categories = Category.objects.all()

    if not user.is_authenticated:
        return HttpResponseRedirect(reverse("index"))

    if request.method == 'POST':
        if not user.is_authenticated:
            return render(request, "auctions/create_auction.html", {
                "error": "Please login to create Auction"
            })
        
        title = request.POST["title"]
        description = request.POST["description"]
        category_id = request.POST["category_id"]
        category = Category.objects.get(pk=category_id)
        start_price = request.POST["start_price"]
        image_url = request.POST["image_url"]
        new_auction = Auction(title=title, description=description,category=category,start_price=start_price,
        image_url=image_url, user=user)
        
        
        new_auction.save()

        messages.success(request, "Auction created successfully.")

        return HttpResponseRedirect(reverse("index"))
        

    return render(request, "auctions/create_auction.html", {
        "categories": categories
    })


def view_auction(request, auction_id):
    auction = Auction.objects.get(pk=auction_id)
    comments = Comment.objects.all().filter(auction=auction_id)
    bids = auction.auction_bids.all()
    user = request.user
    is_watching = auction in user.watchlist.all() if user.is_authenticated else False
    
    return render(request, "auctions/view_auction.html",{
        "auction": auction,
        "comments": comments,
        "bids": len(bids),
        "user": request.user,
        "is_watching": is_watching
    })


def place_bid(request, auction_id):
    if not request.user.is_authenticated:
        messages.error(request, "Please login to bid an Auction.")
        return HttpResponseRedirect(reverse("view_auction", args=(auction_id,)),)

    if request.method == "POST":
        auction = Auction.objects.get(pk=auction_id)
        user = request.user
        amount = request.POST["amount"]
       
        bid = Bid(auction=auction, user=user, amount=amount)
        bid.save()
        auction.highest_bid = bid
        auction.save()
        messages.success(request, "Bid placed successfully.")
        
        return HttpResponseRedirect(reverse("view_auction", args=(auction_id,)))

def place_comment(request, auction_id):
    if not request.user.is_authenticated:
        messages.error(request, "Please login to comment an Auction.")
        return HttpResponseRedirect(reverse("view_auction", args=(auction_id,)),)

    if request.method == "POST":
        message = request.POST["message"]
        auction = Auction.objects.get(pk=auction_id)
        user = request.user
        comment = Comment(message=message, auction=auction, user=user)
        comment.save()

        messages.success(request, "Comment placed successfully.")
        
        return HttpResponseRedirect(reverse("view_auction", args=(auction_id,)))



def watchlist(request, auction_id):
    if request.method == "POST":
        user = request.user        
       
        if not user.is_authenticated:
            messages.error(request, "Please login to add Auction to watchlist.")
            return HttpResponseRedirect(reverse("view_auction", args=(auction_id,)),)
            

        auction = Auction.objects.get(pk=auction_id)
        
        if auction in user.watchlist.all():
            user.watchlist.remove(auction)
        else:
            user.watchlist.add(auction)
    
        user.save()
        
        return HttpResponseRedirect(reverse("view_auction", args=(auction_id,)))


def list_watchlist(request):
    user = request.user
    auctions = user.watchlist.all()
    return render(request, "auctions/watchlist.html",{
        "auctions": auctions
    })

def close_auction(request, auction_id):
    if request.method == "POST":
        if not request.user.id == Auction.objects.get(pk=auction_id).user.id:
            messages.error(request, "You are not authorized to close this Auction.")
            return HttpResponseRedirect(reverse("view_auction", args=(auction_id,)),)

        auction = Auction.objects.get(pk=auction_id)
        auction.is_active = False
        auction.save()
        
        messages.success(request, "Auction closed successfully.")
        return HttpResponseRedirect(reverse("view_auction", args=(auction_id,)))


def list_categories(request):
    categories = Category.objects.all()
    return render(request, "auctions/categories.html",{
        "categories": categories
    })
