from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render
from django.urls import reverse
from .models import User, Bid, Comment, AuctionList, Watchlist, Category
from django.db.models import Max
from django import forms

class NewAuctionForm(forms.Form):
    auctionName = forms.CharField(label = "Nueva subasta")
    auctionDescription = forms.CharField(label = "Descripción")
    initialBid = forms.IntegerField()
    auctionImg = forms.URLField(required=False)
    category = forms.CharField(label="Categoria")

class NewBidForm(forms.Form):
    bid = forms.IntegerField()

class NewCommentForm(forms.Form):
    comment = forms.CharField(widget=forms.Textarea)


# Show all active auctions in index page
def index(request):
    x = AuctionList.objects.all().filter(status=True)
    print(x)

    return render(request, "auctions/index.html", {
        "auctions": x
        })


# Authentication function
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
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


# Logout function
@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


# Register in the site
def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


# Create a new auction
@login_required
def create(request):
    if request.method == "POST":
        form = NewAuctionForm(request.POST)
        print(form.errors)
        if form.is_valid():
            auctionName = form.cleaned_data["auctionName"]
            auctionDescription = form.cleaned_data["auctionDescription"]
            auctionImg = form.cleaned_data["auctionImg"]
            initialBid = form.cleaned_data["initialBid"]
            category = form.cleaned_data["category"]

            eq = AuctionList(user=request.user, auction=auctionName, description=auctionDescription, img=auctionImg, oferta=initialBid, categoria=category)
            eq.save()

            eg = Bid(user=request.user, bid=initialBid, auctionid=eq.id)
            eg.save()

            ec = Category(category=category)
            ec.save()

            return HttpResponseRedirect(reverse("index"))

        else:
            return HttpResponseNotFound("Error in form validation")


    else:
        form = NewAuctionForm()
        return render(request, "auctions/create.html", {
            "form": form
            })

# Showing a auction
def listingpage(request, listing):
    if request.method == "POST":
        return HttpResponseNotFound("Go back")

    else:
        publicacion = AuctionList.objects.get(auction__iexact=str(listing))
        ultimaoferta = Bid.objects.all().filter(auctionid=publicacion.id).aggregate(Max('bid'))
        ultimaoferta = ultimaoferta["bid__max"] # Extract the number of dictionary
        bidform = NewBidForm()
        seguimiento = Watchlist.objects.filter(user=request.user, auctionid=publicacion.id)

        # Determines if the user owns the auction
        user = request.user
        if str(user) == str(publicacion.user):
            owner = True
        else:
            owner = False
        owner = bool(owner)

        # Determines whether the publication is active or not
        status = publicacion.status     

        # Enable the comment form
        if user:
            comment_form = NewCommentForm()

        # Determines if the logged user has won the auction
        if publicacion.status == False and str(publicacion.winneruser) == str(request.user):
            c = Comment.objects.filter(auctionid=publicacion.id)
            winner_message = f"Felicitaciones! Vos, {request.user} has ganado la subasta."
            return render(request, "auctions/listingpage.html", {
                "item":publicacion, "ultimaoferta":ultimaoferta, "status":status, "winner_message": winner_message, "comment_form":comment_form, "comentarios":c
                })


        # Find the comments that the publication already has
        c = Comment.objects.filter(auctionid=publicacion.id)

        return render(request, "auctions/listingpage.html", {
         "item":publicacion, "seguimiento":bool(seguimiento), "bidform":bidform, "owner":owner,
          "ultimaoferta":ultimaoferta, "status":status, "comment_form":comment_form, "comentarios":c })


@login_required
def watchlist(request, item_id):

	# Indentifying auction in watchlist of the user
    identifier = item_id
    x = AuctionList.objects.get(id=identifier)
    seguimiento = Watchlist.objects.filter(user=request.user, auctionid=item_id)
    

    ultimaoferta = Bid.objects.all().filter(auctionid=item_id).aggregate(Max('bid'))
    ultimaoferta = ultimaoferta["bid__max"]


    # Determines if the user owns the auction
    user = request.user
    if str(user) == str(x.user):
        owner = True
    else:
        owner = False

    # If auction is in Watchlist, delete
    if seguimiento:
        seguimiento.delete()
        return HttpResponseRedirect(reverse("listingpage", args=(x.auction,)))

    # Else, add
    else:
        t = Watchlist(user=request.user, auctionid=identifier, auction=x.auction)
        t.save()
        return HttpResponseRedirect(reverse("listingpage", args=(x.auction,)))


# Watchlist page
@login_required
def watchlist2(request, user):
    watchlist = Watchlist.objects.filter(user=user)
    return render(request, "auctions/watchlist.html", {"watchlist":watchlist})

# Display categories
def categories(request):
    categories = Category.objects.all()
    return render(request, "auctions/categories.html" , {"categories":categories})

# Display items in a specific category
def categories2(request, category):
    categories = AuctionList.objects.filter(categoria=category)
    return render(request, "auctions/categories2.html", {"categories":categories, "category":category})

# Bid function
@login_required
def bid(request, item_id):
    if request.method == "POST":
        x = AuctionList.objects.get(id=item_id)
        seguimiento = Watchlist.objects.filter(user=request.user, auctionid=item_id)
        status = x.status
        form = NewBidForm(request.POST)
        if form.is_valid():
            bid = int(form.cleaned_data["bid"])

   			# Determines if the user owns the auction
            user = request.user
            if str(user) == str(x.user):
                owner = True
            else:
                owner = False

            # Enable the comment form
            if user:
            	comment_form = NewCommentForm()

            # Find the comments that the publication already has
            c = Comment.objects.filter(auctionid=x.id)

            # If there is already a bigger bet
            if Bid.objects.filter(bid__gt=bid, auctionid=item_id):
                ultimaoferta = Bid.objects.all().filter(auctionid=item_id).aggregate(Max('bid'))
                ultimaoferta = ultimaoferta["bid__max"]
                bidform = NewBidForm()
                return render(request, "auctions/listingpage.html", {
                    "item":x, "seguimiento":bool(seguimiento), "bidform":bidform, "ultimaoferta":ultimaoferta, "message":"Tu oferta es muy baja", "owner":owner, "status":status, "comment_form":comment_form, "comentarios":c
                    })

            # If there isn't already a bigger bet
            else:
                bidform = NewBidForm()
                b = Bid(user=request.user, bid=bid, auctionid=item_id)
                b.save()
                o = AuctionList.objects.get(id=item_id)
                o.oferta = bid
                o.save()
                ultimaoferta = Bid.objects.all().filter(auctionid=item_id).aggregate(Max('bid'))
                ultimaoferta = ultimaoferta["bid__max"]
                return render(request, "auctions/listingpage.html", {
                    "item":x, "seguimiento":bool(seguimiento), "bidform":bidform, "ultimaoferta": ultimaoferta, "message":f"Has pujado {bid} monedas por este producto", "owner":owner, "status":status, "comment_form":comment_form, "comentarios": c
                    })

        else:
            return HttpResponseNotFound("Nos hemos perdido en la selva, vuelve atrás")            


    else:
        return HttpResponseNotFound("Nos hemos perdido en el castillo, vuelve atrás")

# Function to determine if auction is active or not
@login_required
def status(request, item_id):
    item = AuctionList.objects.get(id=item_id)
    if item.status == True:
        item.status = False
        item.save()
        return HttpResponseRedirect(reverse("listingpage", args=(item.auction,)))
    else:
        item.status = True
        item.save()
        return HttpResponseRedirect(reverse("listingpage", args=(item.auction,)))



# Comment a auction
@login_required
def comment(request, item_id):
    if request.method == "POST":
        form = NewCommentForm(request.POST)
        if form.is_valid():
            comment = form.cleaned_data["comment"]
            newcomment = Comment(user=request.user, comment=comment, auctionid=item_id)
            newcomment.save()
            return HttpResponseRedirect(reverse("index"))
