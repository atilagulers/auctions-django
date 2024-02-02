from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    watchlist = models.ManyToManyField('Auction', blank=True, related_name="watch_list")

    def __str__(self):
        return f"{self.username}"
    
class Category(models.Model):
    title = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.title}"


class Auction(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=256)
    imageUrl = models.CharField(max_length=1000)
    highest_bid = models.ForeignKey("Bid", on_delete=models.DO_NOTHING, related_name="bid_price")
    user = models.ForeignKey("User", on_delete=models.DO_NOTHING, related_name='user_actions')
    category = models.ForeignKey("Category", on_delete=models.DO_NOTHING, related_name='category_auctions')
    isActive = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.title} - ${self.highest_bid.amount} - ({self.category})"



class Bid(models.Model):
    auction = models.ForeignKey('Auction', on_delete=models.CASCADE, related_name="auction_bids")
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="user_bids")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.full_name} - {self.auction.title} - ${self.amount}"
 