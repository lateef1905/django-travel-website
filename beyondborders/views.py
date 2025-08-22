from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import ListView, DetailView
from django.utils.decorators import method_decorator
from django.db.models import Q
from .models import Destination, Booking
from .forms import BookingForm

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
    
    def get_queryset(self):
        # Order by offer status (True first) then alphabetically by name
        return Destination.objects.all().order_by('-offer', 'name')

class DestinationDetailView(DetailView):
    model = Destination
    template_name = 'destination_detail.html'
    context_object_name = 'destination'

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
