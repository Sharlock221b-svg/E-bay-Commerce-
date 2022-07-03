from datetime import datetime
from itertools import product
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass


class auctionProduct(models.Model):
    """This is a Product models containing column's :
      * title=> 
      * description=>
      * price=>
      * category=>
      * image_url=> url field OPTIONAL
      * time=> default now()
      * active=> boolean
      * creator=> Fk User
    """
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=2000)
    price = models.IntegerField()
    category = models.CharField(max_length=15)
    image_url = models.URLField(blank=True,max_length=500)
    time = models.DateTimeField(default=datetime.utcnow())
    active = models.BooleanField(default=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="products",null=True)

    def __str__(self):
        return f"{self.title}: {self.price} created"


class Bids(models.Model):
    """ This is a Bids Model containing:
       * top_bid=> highest bid on a product
       * time=> time of the bid
       * product=> Fk product of bidding
       * bidder=> Fk references to the User
    """
    top_bid = models.IntegerField()
    time = models.DateTimeField(default=datetime.utcnow())
    bider = models.ForeignKey(User,on_delete=models.CASCADE, related_name="userBids", null=True)
    product = models.ForeignKey(auctionProduct,on_delete=models.CASCADE, related_name="productBids")
    

class Comment(models.Model):
    """This is a Comment model containing:
       * comment=> comment
       * time=>curent One
       * product=>Fk
       * commenter=>Fk
    """
    comment = models.CharField(max_length=1000)
    time = models.DateTimeField(default=datetime.utcnow())
    commenter = models.ForeignKey(User,on_delete=models.CASCADE, related_name="userComment")
    product = models.ForeignKey(auctionProduct,on_delete=models.CASCADE, related_name="productComment")


class Wishlist(models.Model):
    """This is a Wishlist model containing:
       * User => Fk
       * Product => Fk
    """
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(auctionProduct,on_delete=models.CASCADE)
