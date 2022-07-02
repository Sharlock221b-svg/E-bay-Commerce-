from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import User,auctionProduct
from django import forms
from datetime import datetime

CATEGORIES = [
    ('fashion','Fashion'),
    ('toy', 'Toys'),
    ('electronics', 'Electronics'),
    ('home', 'Home'),
    ('books','Books'),
    ('coumputers','Computers'),
    ('real estate', 'Real Estate'),
    ('sports', 'Sports')
]

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
        widget=forms.Select(
            attrs={"class": "form-control"},
            choices=CATEGORIES
        )
    )
    imgUrl = forms.URLField(
        required=False,
        label="Image URL",
        widget=forms.URLInput(
            attrs={"class": "form-control", "placeholder": "Image URL"}
        )
    )


def index(request):

    return render(request, "auctions/index.html",{
        "products": auctionProduct.objects.filter(active=True).values()
    })


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


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


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


@login_required(login_url='login')
def createListing(request):
    if request.method == "POST":
       form = createNew(request.POST)

       if form.is_valid():
         p = auctionProduct(
            title=form.cleaned_data["title"],
            description=form.cleaned_data["description"],
            price=form.cleaned_data["price"],
            category=form.cleaned_data["category"],
            image_url=form.cleaned_data["imgUrl"]
         )
         p.save()
         return HttpResponseRedirect(reverse("index"))
       else:
          return HttpResponse("Invalid Data Filled!!")
    return render(request, "auctions/create.html", {"form": createNew()})
