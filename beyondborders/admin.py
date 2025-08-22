from django.contrib import admin
from .models import Destination, Booking

# Register your models here.

@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'offer')
    list_filter = ('offer',)
    search_fields = ('name', 'desc')

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'destination', 'travel_date', 'number_of_travelers', 'status', 'created_at')
    list_filter = ('status', 'created_at', 'travel_date')
    search_fields = ('user__username', 'destination__name')
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at',)
