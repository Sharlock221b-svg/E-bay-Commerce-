from datetime import datetime
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class auctionProduct(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    price = models.IntegerField()
    category = models.CharField(max_length=15)
    image_url = models.URLField(blank=True,max_length=500)
    time = models.DateTimeField(default=datetime.utcnow())

   # created_by = models.ManyToOneRel(User, base=CASCADE)
    def __str__(self):
        return f"{self.title}: {self.price} created"
