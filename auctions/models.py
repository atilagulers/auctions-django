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
    image_url = models.CharField(max_length=1000)
    start_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    highest_bid = models.ForeignKey("Bid", on_delete=models.DO_NOTHING, related_name="bid_price", blank=True, null=True)
    user = models.ForeignKey("User", on_delete=models.DO_NOTHING, related_name='user_actions')
    category = models.ForeignKey("Category", on_delete=models.DO_NOTHING, related_name='category_auctions')
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        highest_bid_amount = self.highest_bid.amount if self.highest_bid else self.start_price
        return f"{self.title} - ${highest_bid_amount} - ({self.category})"



class Bid(models.Model):
    auction = models.ForeignKey('Auction', on_delete=models.CASCADE, related_name="auction_bids")
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="user_bids")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.amount}"
 

class Comment(models.Model):
    message = models.CharField(max_length=256)
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name = 'user_comments')
    auction = models.ForeignKey("Auction", on_delete=models.CASCADE, related_name='auction_comments', default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
