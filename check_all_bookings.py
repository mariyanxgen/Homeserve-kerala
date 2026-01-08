import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'homeserve.settings')
django.setup()

from services.models import Booking, Payment, ProviderEarnings
from decimal import Decimal

# Get all completed bookings
completed_bookings = Booking.objects.filter(status='completed').order_by('-completed_at')

print(f"Total completed bookings: {completed_bookings.count()}\n")

for booking in completed_bookings:
    print(f"{'='*60}")
    print(f"Booking #{booking.id}")
    print(f"Service: {booking.service.title}")
    print(f"Customer: {booking.customer_name}")
    print(f"Amount: ₹{booking.service.price}")
    print(f"Completed: {booking.completed_at}")
    
    # Check payment
    try:
        payment = Payment.objects.get(booking=booking)
        print(f"✓ Payment exists: ₹{payment.amount} - Status: {payment.status}")
    except Payment.DoesNotExist:
        print(f"✗ NO PAYMENT RECORD")
        payment = None
    
    # Check earnings
    if hasattr(booking, 'provider_earning'):
        earning = booking.provider_earning
        print(f"✓ Earnings exist: Net ₹{earning.net_amount}")
    else:
        print(f"✗ NO EARNINGS RECORD")
        
        # Try to create if payment exists
        if payment and payment.status == 'completed':
            print(f"  → Creating earnings now...")
            
            commission_percentage = Decimal('10.00')
            gross_amount = payment.amount
            commission_amount = (gross_amount * commission_percentage) / Decimal('100.00')
            net_amount = gross_amount - commission_amount
            
            earning = ProviderEarnings.objects.create(
                provider=booking.provider,
                booking=booking,
                payment=payment,
                gross_amount=gross_amount,
                commission_percentage=commission_percentage,
                commission_amount=commission_amount,
                net_amount=net_amount,
                payout_status='pending'
            )
            print(f"  ✓ Created: Gross ₹{gross_amount} → Net ₹{net_amount}")
        elif payment:
            print(f"  → Payment status is '{payment.status}' (needs 'completed')")
        else:
            print(f"  → Cannot create earnings without payment")
    
    print()

print(f"{'='*60}")
print("SUMMARY:")
all_earnings = ProviderEarnings.objects.all()
from django.db.models import Sum
total = all_earnings.aggregate(total=Sum('net_amount'))['total'] or 0
pending = all_earnings.filter(payout_status='pending').aggregate(total=Sum('net_amount'))['total'] or 0
print(f"Total earnings records: {all_earnings.count()}")
print(f"Total net amount: ₹{total}")
print(f"Pending payout: ₹{pending}")
