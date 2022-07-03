from datetime import datetime
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass


class auctionProduct(models.Model):
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
