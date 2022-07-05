from unicodedata import category
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import User, auctionProduct, Wishlist, Bids, Comment
from django import forms
from datetime import datetime

#List of categories
CATEGORIES = [
    ("fashion", "Fashion"),
    ("toy", "Toys"),
    ("electronics", "Electronics"),
    ("home", "Home"),
    ("books", "Books"),
    ("coumputers", "Computers"),
    ("real estate", "Real Estate"),
    ("sports", "Sports"),
    ("eatery", "Eatery"),
    ("study", "Study"),
]

global_var = {
    "res": None,
}
#Form for creating new Product
class createNew(forms.Form):
    title = forms.CharField(
        max_length=100,
        min_length=2,
        widget=forms.TextInput(attrs={"placeholder": "Title", "class": "form-control"}),
    )
    description = forms.CharField(
        min_length=15,
        max_length=1000,
        widget=forms.Textarea(
            attrs={"placeholder": "Description", "class": "form-control"}
        ),
    )
    price = forms.IntegerField(
        min_value=1,
        label="Price $",
        widget=forms.NumberInput(
            attrs={"placeholder": "Base Bid", "class": "form-control"}
        ),
    )
    category = forms.CharField(
        label="Category",
        widget=forms.Select(attrs={"class": "form-control"}, choices=CATEGORIES),
    )
    imgUrl = forms.URLField(
        required=False,
        label="Image URL",
        widget=forms.URLInput(
            attrs={"class": "form-control", "placeholder": "Image URL"}
        ),
    )

#Form for Bidding
class BidForm(forms.Form):
    top_bid = forms.IntegerField(
        label="Place Your Bid",
        min_value=1,
        widget=forms.NumberInput(
            attrs={"class": "form-control", "placeholder": "Bid $"}
        ),
    )

#Form for posting comment
class CommentForm(forms.Form):
    Comment = forms.CharField(
        min_length=3,
        max_length=1000,
        widget=forms.Textarea(
            attrs={"placeholder": "Comment", "class": "form-control", "rows": 4}
        ),
    )

#Index function renders the active products to the page
def index(request):
    return render(
        request,
        "auctions/index.html",
        {"products": auctionProduct.objects.filter(active=True).order_by("-time").values()},
    )


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(
                request,
                "auctions/login.html",
                {"message": "Invalid username and/or password."},
            )
    else:
        return render(request, "auctions/login.html")

#Logout Function
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

#Registration
def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(
                request, "auctions/register.html", {"message": "Passwords must match."}
            )

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(
                request,
                "auctions/register.html",
                {"message": "Username already taken."},
            )
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


@login_required(login_url="login")
def createListing(request):
    """ If called vis post validates the product data and
        save it to the database.
        Else if called via get the then renders the createNew Form.
    """
    if request.method == "POST":
        form = createNew(request.POST)

        if form.is_valid():
            p = auctionProduct(
                title=form.cleaned_data["title"],
                description=form.cleaned_data["description"],
                price=form.cleaned_data["price"],
                category=form.cleaned_data["category"],
                image_url=form.cleaned_data["imgUrl"],
                creator=User.objects.get(pk=request.user.id),
            )
            p.save()
            return HttpResponseRedirect(reverse("index"))
        else:
            return HttpResponse("Invalid Data Filled!!")
    return render(request, "auctions/create.html", {"form": createNew()})


def listing(request, id):
    product = auctionProduct.objects.get(pk=id)
    hearted = True
    # Wishlist Query
    try:
        user = User.objects.get(pk=request.user.id)
        wish = Wishlist.objects.get(user=user, product=product)
    except:
        hearted = False

    q = Bids.objects.filter(product=product).order_by("-top_bid").first()
    no_bids = Bids.objects.filter(product=product).count()

    res = global_var["res"]
    global_var["res"] = None

    try:
        top_bid = q.top_bid
        bider = q.bider
    except:
        top_bid = None
        bider = None

    comments = Comment.objects.filter(product=product).order_by("-time")

    return render(
        request,
        "auctions/listing.html",
        {
            "product": product,
            "wish": hearted,
            "Bid": BidForm(),
            "res": res,
            "highest_bid": top_bid,
            "count": no_bids,
            "bidder": bider,
            "CommentForm": CommentForm(),
            "comments": comments,
        },
    )


@login_required(login_url="login")
def addWish(request):
    if request.method == "POST":
        user = User.objects.get(pk=request.user.id)
        product = auctionProduct.objects.get(pk=request.POST["p_id"])
        try:
            w = Wishlist(user=user, product=product)
            w.save()
        except IntegrityError:
            return HttpResponse("Product has been already there on your Wishlist.")
        return HttpResponseRedirect(reverse("listing", args=(request.POST["p_id"],)))


@login_required(login_url="login")
def removeWish(request):
    if request.method == "POST":
        user = User.objects.get(pk=request.user.id)
        product = auctionProduct.objects.get(pk=request.POST["p_id"])
        try:
            Wishlist.objects.filter(user=user, product=product).delete()
        except IntegrityError:
            return HttpResponse("Product has been already removed from your Wishlist.")
        return HttpResponseRedirect(reverse("listing", args=(request.POST["p_id"],)))


@login_required(login_url="login")
def bid(request, id):
    if request.method == "POST":
        print(id)
        form = BidForm(request.POST)
        if form.is_valid():
            top_bid = form.cleaned_data["top_bid"]
            print(top_bid)
            user = User.objects.get(pk=request.user.id)
            product = auctionProduct.objects.get(pk=id)
            q = (
                Bids.objects.filter(product=product)
                .only("top_bid")
                .order_by("-top_bid")
                .first()
            )

            if q is not None:
                # print("above")
                if top_bid > q.top_bid:
                    global_var["res"] = "High"
                    q = Bids(top_bid=top_bid, bider=user, product=product)
                    q.save()
                else:
                    global_var["res"] = "Low"
            else:
                # print("below")
                if top_bid > product.price:
                    global_var["res"] = "High"
                    q = Bids(top_bid=top_bid, bider=user, product=product)
                    q.save()
                else:
                    global_var["res"] = "Low"

            return HttpResponseRedirect(reverse("listing", args=(id,)))


@login_required(login_url="login")
def closeAuction(request, id):
    if request.method == "POST":
        product = auctionProduct.objects.get(pk=id)
        q = Bids.objects.filter(product=product).order_by("-top_bid").first()
        product.active = False
        product.winner = User.objects.get(pk=q.bider.id)
        product.save()
        Wishlist.objects.filter(product=product).delete()
        return HttpResponseRedirect(reverse("listing", args=(id,)))


@login_required(login_url="login")
def addComment(request, id):
    if request.method == "POST":
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.cleaned_data["Comment"]
            product = auctionProduct.objects.get(pk=id)
            user = User.objects.get(pk=request.user.id)
            q = Comment(comment=comment, commenter=user, product=product)
            q.save()
            return HttpResponseRedirect(reverse("listing", args=(id,)))
        else:
            return HttpResponse("Invalid Form Entry!!")


@login_required(login_url="login")
def watchlist(request):
    user = User.objects.get(pk=request.user.id)
    q = Wishlist.objects.filter(user=user).values()
    product_id = []
    for i in q:
        product_id.append(i["product_id"])
    products = auctionProduct.objects.filter(id__in=product_id)
    print(products)
    return render(request, "auctions/watchlist.html", {"products": products})


def categories(request):
    return render(request, "auctions/categories.html", {"categories": CATEGORIES})


def getProduct(request, name):
    products = auctionProduct.objects.filter(category=name,active=True)
    return render(
        request,
        "auctions/index.html",
        {"products": products},
    )
