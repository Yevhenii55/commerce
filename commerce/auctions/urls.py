from django.urls import path

from . import views



urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_auction", views.create_auction, name="create_auction"),
    path('auction_detail/<int:auction_id>/', views.auction_detail, name='auction_detail'),
    path('place_bid/<int:auction_id>/', views.place_bid, name='place_bid'),
    path('auctions/<int:auction_id>/toggle-watchlist/', views.toggle_watchlist, name='toggle_watchlist'),
    path('watchlist/', views.watchlist, name='watchlist'),
    path('registration/', views.register, name='registration'),
    path('add_comment/<int:auction_id>/', views.add_comment, name='add_comment'),
    path('auction_detail/<int:auction_id>/', views.auction_detail, name='auction_detail'),
    path('auction_detail/<int:auction_id>/close/', views.close_auction, name='close_auction'),
    path('categories/', views.category_list, name='category_list'),
    path('categories/<int:category_id>/', views.active_auctions, name='active_auctions'),

]

