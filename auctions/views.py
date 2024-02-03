from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
 
from .models import User, Auction, Category, Bid


def index(request):
    auctions = Auction.objects.all().filter(is_active=True)
    print(auctions)
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
            return render(request, "auctions/create.html", {
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

        return HttpResponseRedirect(reverse("index"))
        

    return render(request, "auctions/create_auction.html", {
        "categories": categories
    })


def view_auction(request, auction_id):
    auction = Auction.objects.get(pk=auction_id)



  
    
    return render(request, "auctions/view_auction.html",{
        "auction": auction
    })
