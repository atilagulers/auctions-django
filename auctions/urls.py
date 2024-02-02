from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("auctions/create", views.create_auction, name="create_auction"),
    path("auctions/<int:auction_id>", views.view_auction, name="view_auction")
]
