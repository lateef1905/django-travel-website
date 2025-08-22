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
]
