#!/usr/bin/env python
"""
Data migration script to copy data from travello to beyondborders
"""
import os
import sys
import django

# Add the project directory to the path
sys.path.append('/path/to/firstprogram')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'firstprogram.settings')
django.setup()

from travello.models import Destination as OldDestination, Booking as OldBooking
from beyondborders.models import Destination as NewDestination, Booking as NewBooking

def migrate_data():
    print("Starting data migration from travello to beyondborders...")
    
    # Migrate Destinations
    print("Migrating destinations...")
    old_destinations = OldDestination.objects.all()
    destination_mapping = {}
    
    for old_dest in old_destinations:
        new_dest = NewDestination.objects.create(
            name=old_dest.name,
            img=old_dest.img,
            desc=old_dest.desc,
            price=old_dest.price,
            offer=old_dest.offer
        )
        destination_mapping[old_dest.id] = new_dest
        print(f"Migrated destination: {old_dest.name}")
    
    # Migrate Bookings
    print("Migrating bookings...")
    old_bookings = OldBooking.objects.all()
    
    for old_booking in old_bookings:
        new_dest = destination_mapping[old_booking.destination.id]
        NewBooking.objects.create(
            user=old_booking.user,
            destination=new_dest,
            travel_date=old_booking.travel_date,
            number_of_travelers=old_booking.number_of_travelers,
            status=old_booking.status,
            created_at=old_booking.created_at
        )
        print(f"Migrated booking: {old_booking.user.username} - {old_booking.destination.name}")
    
    print("Data migration completed successfully!")
    print(f"Total destinations migrated: {NewDestination.objects.count()}")
    print(f"Total bookings migrated: {NewBooking.objects.count()}")

if __name__ == '__main__':
    migrate_data()
