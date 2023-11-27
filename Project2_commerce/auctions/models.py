from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Listing(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length = 64)
    description = models.TextField()
    starting_bid = models.DecimalField(max_digits = 7, decimal_places=2)
    image = models.URLField()
    category = models.CharField(max_length = 64)
    user = models.CharField(max_length = 64, default = None)
    watchlist = models.ManyToManyField(User, related_name = "user")
    active = models.BooleanField(blank = True, null = True)

class Bid(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.CharField(max_length = 64)
    value = models.DecimalField(max_digits = 7, decimal_places=2)
    listing = models.ForeignKey(Listing, on_delete = models.CASCADE, blank = True, null = True, related_name = "listingBid")

class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.CharField(max_length = 64)
    text = models.TextField()
    listing = models.ForeignKey(Listing, on_delete = models.CASCADE, blank = True, null = True, related_name = "listingComment")


    def __str__(self):
        return self.title
