from django.contrib import admin
from .models import Bid, Comment, AuctionList, Watchlist, Category

# Register your models here.
admin.site.register(Bid)
admin.site.register(Comment)
admin.site.register(AuctionList)
admin.site.register(Watchlist)
admin.site.register(Category)