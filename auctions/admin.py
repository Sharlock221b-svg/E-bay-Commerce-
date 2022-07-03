from django.contrib import admin
from .models import auctionProduct,User,Bids,Comment,Wishlist

# Register your models here.
admin.site.register(auctionProduct)
admin.site.register(User)
admin.site.register(Bids)
admin.site.register(Comment)
admin.site.register(Wishlist)

