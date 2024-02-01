from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    watchlist = models.ManyToManyField('Product', blank=True, related_name="watchers")

    def __str__(self):
        return f"{self.username}"

    
class Product(models.Model):
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=256)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name="products")
    image = models.ImageField(upload_to='images/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name="products")
    



    def __str__(self):
        return f"{self.name} - ${self.price}"


class Category(models.Model):
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=256)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"{self.name}"

class Bid(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name="bids")
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name="bids")
    bid = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"{self.product} - ${self.bid}"
    
    


# auction
# bids
# comments
