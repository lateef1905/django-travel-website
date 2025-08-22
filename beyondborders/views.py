from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import ListView, DetailView
from django.utils.decorators import method_decorator
from django.db.models import Q, Avg
from django.http import JsonResponse
from django.urls import reverse
from .models import Destination, Booking, Review, Wishlist, BlogPost
from .forms import BookingForm, ReviewForm, DestinationSearchForm

# Create your views here.

def index(request):
    # Filter only destinations with special offers (offer=True)
    # Order by offer status (True first) then alphabetically by name
    dests = Destination.objects.filter(offer=True).order_by('name')
    return render(request, 'index.html', {'dests': dests})

class DestinationListView(ListView):
    model = Destination
    template_name = 'destinations.html'
    context_object_name = 'destinations'
    paginate_by = 12
    
    def get_queryset(self):
        queryset = Destination.objects.all()
        form = DestinationSearchForm(self.request.GET)
        
        if form.is_valid():
            query = form.cleaned_data.get('query')
            location = form.cleaned_data.get('location')
            min_price = form.cleaned_data.get('min_price')
            max_price = form.cleaned_data.get('max_price')
            min_rating = form.cleaned_data.get('min_rating')
            offer_only = form.cleaned_data.get('offer_only')
            
            if query:
                queryset = queryset.filter(
                    Q(name__icontains=query) | Q(desc__icontains=query)
                )
            
            if location:
                queryset = queryset.filter(location__icontains=location)
            
            if min_price:
                queryset = queryset.filter(price__gte=min_price)
            
            if max_price:
                queryset = queryset.filter(price__lte=max_price)
            
            if min_rating:
                # Filter destinations with average rating >= min_rating
                queryset = queryset.annotate(
                    avg_rating=Avg('reviews__rating')
                ).filter(avg_rating__gte=int(min_rating))
            
            if offer_only:
                queryset = queryset.filter(offer=True)
        
        # Order by offer status (True first) then alphabetically by name
        return queryset.order_by('-offer', 'name')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = DestinationSearchForm(self.request.GET)
        return context

class DestinationDetailView(DetailView):
    model = Destination
    template_name = 'destination_detail.html'
    context_object_name = 'destination'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        destination = self.get_object()
        
        # Get reviews for this destination
        context['reviews'] = destination.reviews.all()[:10]  # Latest 10 reviews
        context['user_review'] = None
        context['review_form'] = ReviewForm()
        context['is_in_wishlist'] = False
        
        if self.request.user.is_authenticated:
            # Check if user already reviewed this destination
            try:
                context['user_review'] = Review.objects.get(
                    user=self.request.user, 
                    destination=destination
                )
            except Review.DoesNotExist:
                pass
            
            # Check if destination is in user's wishlist
            context['is_in_wishlist'] = Wishlist.objects.filter(
                user=self.request.user, 
                destination=destination
            ).exists()
        
        return context

@login_required
def add_review(request, destination_id):
    """Add or update a review for a destination"""
    destination = get_object_or_404(Destination, id=destination_id)
    
    try:
        # Check if user already has a review for this destination
        review = Review.objects.get(user=request.user, destination=destination)
        form = ReviewForm(request.POST, instance=review)
        action = 'updated'
    except Review.DoesNotExist:
        form = ReviewForm(request.POST)
        action = 'added'
    
    if form.is_valid():
        review = form.save(commit=False)
        review.user = request.user
        review.destination = destination
        review.save()
        
        messages.success(request, f'Your review has been {action} successfully!')
    else:
        messages.error(request, 'Please correct the errors in your review.')
    
    return redirect('destination_detail', pk=destination_id)

@login_required
def toggle_wishlist(request, destination_id):
    """Add or remove destination from user's wishlist"""
    if request.method == 'POST':
        destination = get_object_or_404(Destination, id=destination_id)
        wishlist_item, created = Wishlist.objects.get_or_create(
            user=request.user, 
            destination=destination
        )
        
        if not created:
            # Item already exists, remove it
            wishlist_item.delete()
            action = 'removed'
            in_wishlist = False
        else:
            # Item was created
            action = 'added'
            in_wishlist = True
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            # AJAX request
            return JsonResponse({
                'success': True,
                'action': action,
                'in_wishlist': in_wishlist
            })
        else:
            messages.success(request, f'Destination {action} to wishlist!')
            return redirect('destination_detail', pk=destination_id)
    
    return redirect('destination_detail', pk=destination_id)

@method_decorator(login_required, name='dispatch')
class WishlistView(ListView):
    model = Wishlist
    template_name = 'wishlist.html'
    context_object_name = 'wishlist_items'
    paginate_by = 12
    
    def get_queryset(self):
        return Wishlist.objects.filter(user=self.request.user)

@login_required
def book_destination(request, destination_id):
    destination = get_object_or_404(Destination, id=destination_id)
    
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.destination = destination
            booking.save()
            messages.success(request, 'Your booking has been submitted successfully!')
            return redirect('booking_success', booking_id=booking.id)
    else:
        form = BookingForm()
    
    return render(request, 'booking_form.html', {
        'form': form,
        'destination': destination
    })

@login_required
def booking_success(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    return render(request, 'booking_success.html', {'booking': booking})

@method_decorator(login_required, name='dispatch')
class MyTripsView(ListView):
    model = Booking
    template_name = 'my_trips.html'
    context_object_name = 'bookings'
    paginate_by = 10
    
    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)

def search_destinations(request):
    """
    Search destinations based on name, description, price range, and special offers
    """
    query = request.GET.get('destination', '')
    max_price = request.GET.get('budget', '')
    offer_only = request.GET.get('offer_only', '')
    travel_date = request.GET.get('travel_date', '')
    
    destinations = Destination.objects.all()
    
    # Filter by destination name or description
    if query:
        destinations = destinations.filter(
            Q(name__icontains=query) | Q(desc__icontains=query)
        )
    
    # Filter by maximum price
    if max_price:
        try:
            max_price = int(max_price)
            destinations = destinations.filter(price__lte=max_price)
        except ValueError:
            pass  # Invalid budget, ignore filter
    
    # Filter by special offers only
    if offer_only == 'true':
        destinations = destinations.filter(offer=True)
    
    # Order by offer status (True first) then alphabetically by name
    destinations = destinations.order_by('-offer', 'name')
    
    return render(request, 'search_results.html', {
        'destinations': destinations,
        'query': query,
        'budget': max_price,
        'offer_only': offer_only,
        'travel_date': travel_date,
        'total_results': destinations.count()
    })

# Blog Views
class BlogListView(ListView):
    model = BlogPost
    template_name = 'blog.html'
    context_object_name = 'blog_posts'
    paginate_by = 6
    
    def get_queryset(self):
        return BlogPost.objects.filter(is_published=True)

class BlogDetailView(DetailView):
    model = BlogPost
    template_name = 'blog_detail.html'
    context_object_name = 'post'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    
    def get_queryset(self):
        return BlogPost.objects.filter(is_published=True)
