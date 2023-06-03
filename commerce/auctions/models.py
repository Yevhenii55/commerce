from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    pass





class Category(models.Model):
    name = models.CharField(max_length=100)
   
            
class Auction(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    initial_bid = models.DecimalField(max_digits=10, decimal_places=2)
    image_url = models.URLField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='auctions_created')
    current_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    bids = models.ManyToManyField(User, through='Bid', related_name='bidders', blank=True, through_fields=('auction', 'bidder'))
    winner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='auctions_won')
    winning_bid = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    STATUS_CHOICES = (
        ('active', 'Active'),
        ('closed', 'Closed'),
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')



class Bid(models.Model):
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bids')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    timestamp = models.DateTimeField(default=timezone.now)
    is_winner = models.BooleanField(default=False)


class Comment(models.Model):
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)
    commenter = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"Comment on {self.auction.title} by {self.commenter.username}"
    


class WatchlistItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} - {self.auction.title}"

