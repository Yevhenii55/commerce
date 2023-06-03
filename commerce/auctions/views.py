from django.contrib.auth import authenticate, login, logout, get_user
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import User
from .models import Auction, Category, WatchlistItem, Bid, Comment
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Category

def index(request):
    active_auctions = Auction.objects.filter(end_date__gt=timezone.now())
    message = messages.get_messages(request)
    return render(request, 'auctions/index.html', {'auctions': active_auctions, 'message': message})

def login_view(request):
    if request.method == "POST":

        
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        
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

        
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        
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


def create_categories():
    categories = [
        'Electronics',
        'Books',
        'Clothing',
        'Home & Garden',
        'Toys',
        'Sports',
        'Jewelry',
        'Art',
        'Collectibles',
        'Music',
        'Beauty',
        'Automotive',
        'Health & Wellness',
        'Pets',
        'Food & Drinks',
        'Furniture',
        'Movies',
        'Tools',
        'Travel',
        'Crafts',
        'Electrical Appliances',
        'Outdoor',
        'Office Supplies',
        'Baby',
        'Vintage'
    ]


    for category_name in categories:
        Category.objects.get_or_create(name=category_name)

create_categories()

@login_required(login_url='registration')
def create_auction(request):
    categories = Category.objects.all()
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        initial_bid = request.POST.get('initial_bid')
        image_url = request.POST.get('image_url')
        category_id = request.POST.get('category_id')
        
        if not title or not description or not start_date or not end_date or not initial_bid:
            return HttpResponseBadRequest("Please fill in all required fields.")
        
        category = None
        if category_id:
            try:
                category = Category.objects.get(id=category_id)
            except Category.DoesNotExist:
                return HttpResponseBadRequest("Invalid category.")
        

        auction = Auction.objects.create(
            title=title,
            description=description,
            start_date=start_date,
            end_date=end_date,
            initial_bid=initial_bid,
            image_url=image_url,
            category=category,
            seller=request.user
        )
        
        
        messages.success(request, "Auction created successfully.")
        return redirect('index')
    
    
    return render(request, 'auctions/create_auction.html', {'categories': categories})


def auction_detail(request, auction_id):
    auction = get_object_or_404(Auction, pk=auction_id)
    bids = auction.bids.all()
    item = auction.watchlistitem_set.filter(user=request.user).first() if request.user.is_authenticated else None

    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            if request.user.is_authenticated:
                comment = Comment.objects.create(auction=auction, commenter=request.user, content=content)
                

    comments = Comment.objects.filter(auction=auction).order_by('timestamp')

    return render(request, 'auctions/auction_detail.html', {'auction': auction, 'bids': bids, 'watchlist_item': item, 'comments': comments})


def add_comment(request, auction_id):
    auction = Auction.objects.get(pk=auction_id)

    if request.method == 'POST':
        content = request.POST.get('content')
        commenter = request.user
        Comment.objects.create(auction=auction, commenter=commenter, content=content)
        return redirect('auction_detail', auction_id=auction_id)

    return render(request, 'auctions/add_comment.html', {'auction': auction})



def place_bid(request, auction_id):
    auction = get_object_or_404(Auction, id=auction_id)
    user = request.user
    
    if request.method == 'POST':
        bid_amount = request.POST.get('bid_amount')
        
        
        if not user.is_authenticated:
            messages.error(request, 'You must be logged in to place a bid.')
            return redirect('auction_detail', auction_id=auction.id)
        
        
        if float(bid_amount) <= auction.initial_bid:
            messages.error(request, 'Your bid amount must be greater than the current bid.')
            return redirect('auction_detail', auction_id=auction.id)
        
        
        if auction.seller == user:
            messages.error(request, 'You cannot bid on your own auction.')
            return redirect('auction_detail', auction_id=auction.id)
        
        
        if auction.initial_bid and float(bid_amount) <= auction.initial_bid:
            messages.error(request, 'Your bid amount must be greater than the current bid.')
            return redirect('auction_detail', auction_id=auction.id)
        
        
        bid = Bid.objects.create(auction=auction, bidder=user, amount=bid_amount)
        auction.initial_bid = bid.amount
        auction.save()
        
        messages.success(request, 'Your bid has been placed.')
        
        return redirect('auction_detail', auction_id=auction.id)
    
    return render(request, 'auctions/place_bid.html', {'auction': auction})


@login_required(login_url='registration')
def toggle_watchlist(request, auction_id):
    auction = get_object_or_404(Auction, pk=auction_id)

    try:
        
        item = WatchlistItem.objects.get(user=request.user, auction=auction)
        item.delete()
    except WatchlistItem.DoesNotExist:
        
        item = WatchlistItem(user=request.user, auction=auction)
        item.save()

    
    return HttpResponseRedirect(reverse('auction_detail', args=[auction_id]))


@login_required(login_url='registration')
def watchlist(request):
  
    watchlist_items = WatchlistItem.objects.filter(user=request.user)

    context = {
        'watchlist_items': watchlist_items
    }

    return render(request, 'auctions/watchlist.html', context)



def close_auction(request, auction_id):
    auction = get_object_or_404(Auction, pk=auction_id)
    
    if request.method == 'POST' and request.user == auction.seller:
        if auction.status == 'active':
            auction.status = 'closed'
            highest_bid = auction.bid_set.order_by('-amount').first()
            if highest_bid:
                auction.winner = highest_bid.bidder
                auction.winning_bid = highest_bid.amount
            auction.save()
            messages.success(request, 'The auction has been closed.')
            return redirect('auction_detail', auction_id=auction_id)
        else:
            messages.error(request, 'The auction is not active.')
    else:
        messages.error(request, 'Failed to close the auction.')
    
    return redirect('auction_detail', auction_id=auction_id)


@login_required(login_url='registration')
def category_list(request):
    categories = Category.objects.all()
    return render(request, 'auctions/category_list.html', {'categories': categories})

def active_auctions(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    active_auctions = Auction.objects.filter(category=category, end_date__gt=timezone.now())
    return render(request, 'auctions/active_auctions.html', {'category': category, 'active_auctions': active_auctions})


