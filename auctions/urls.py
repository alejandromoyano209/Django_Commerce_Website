from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("listingpage/<str:listing>", views.listingpage, name="listingpage"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("categories", views.categories, name="categories"),
    path("categories2/<str:category>", views.categories2, name="categories2"),
    path("status/<int:item_id>", views.status, name="status"),
    path("bid/<int:item_id>", views.bid, name="bid"),
    path("watchlist/<int:item_id>", views.watchlist, name="watchlist"),
    path("watchlist2/<str:user>", views.watchlist2, name="watchlist2"),
    path("comment/<int:item_id>", views.comment, name="comment")
]
