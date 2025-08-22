from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('destinations/', views.DestinationListView.as_view(), name='destinations'),
    path('destination/<int:pk>/', views.DestinationDetailView.as_view(), name='destination_detail'),
    path('book/<int:destination_id>/', views.book_destination, name='book_destination'),
    path('booking-success/<int:booking_id>/', views.booking_success, name='booking_success'),
    path('my-trips/', views.MyTripsView.as_view(), name='my_trips'),
    path('search/', views.search_destinations, name='search_destinations'),
    
    # Phase 2 URLs
    path('review/<int:destination_id>/', views.add_review, name='add_review'),
    path('wishlist/toggle/<int:destination_id>/', views.toggle_wishlist, name='toggle_wishlist'),
    path('wishlist/', views.WishlistView.as_view(), name='wishlist'),
    path('blog/', views.BlogListView.as_view(), name='blog'),
    path('blog/<slug:slug>/', views.BlogDetailView.as_view(), name='blog_detail'),
]
