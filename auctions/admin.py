from django.contrib import admin
from .models import auctionProduct,User

# Register your models here.
admin.site.register(auctionProduct)
admin.site.register(User)