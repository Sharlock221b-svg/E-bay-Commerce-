from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("createListing", views.createListing, name="createListing"),
    path("listing/<int:id>", views.listing, name="listing"),
    path("addWishlist", views.addWish, name="addWish"),
    path("removeWishlist", views.removeWish, name="removeWish"),
    path("bid/<int:id>", views.bid, name="bid"),
    path("closeAuction/<int:id>", views.closeAuction, name="closeAuction"),
    path("addComment,<int:id>", views.addComment, name="addComment"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("categories", views.categories, name="Categories"),
    path("getProduct/<str:name>",  views.getProduct, name="getProduct")
]
