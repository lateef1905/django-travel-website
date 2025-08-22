from django.contrib import admin
from .models import Destination, Booking, Review, Wishlist, BlogPost

# Register your models here.

@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'currency', 'location', 'offer', 'average_rating', 'review_count')
    list_filter = ('offer', 'currency', 'location')
    search_fields = ('name', 'desc', 'location')
    readonly_fields = ('average_rating', 'review_count')

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'destination', 'travel_date', 'number_of_travelers', 'status', 'created_at')
    list_filter = ('status', 'created_at', 'travel_date')
    search_fields = ('user__username', 'destination__name')
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at',)

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'destination', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('user__username', 'destination__name', 'comment')
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ('user', 'destination', 'added_at')
    list_filter = ('added_at',)
    search_fields = ('user__username', 'destination__name')
    date_hierarchy = 'added_at'

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'is_published', 'created_at')
    list_filter = ('is_published', 'created_at', 'author')
    search_fields = ('title', 'content')
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at', 'updated_at')
    prepopulated_fields = {'slug': ('title',)}
