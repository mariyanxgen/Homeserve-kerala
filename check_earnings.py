import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'homeserve.settings')
django.setup()

from services.models import Booking, Payment, ProviderEarnings

# Get all completed bookings
completed_bookings = Booking.objects.filter(status='completed')
print(f"Total completed bookings: {completed_bookings.count()}")

for booking in completed_bookings:
    print(f"\n--- Booking #{booking.id} ---")
    print(f"Service: {booking.service.title}")
    print(f"Provider: {booking.provider.business_name}")
    print(f"Customer: {booking.customer_name}")
    print(f"Status: {booking.status}")
    print(f"Completed at: {booking.completed_at}")
    
    # Check if payment exists
    try:
        payment = Payment.objects.get(booking=booking)
        print(f"Payment exists: YES")
        print(f"Payment ID: {payment.id}")
        print(f"Payment Amount: ₹{payment.amount}")
        print(f"Payment Status: {payment.status}")
    except Payment.DoesNotExist:
        print("Payment exists: NO")
        payment = None
    
    # Check if earnings record exists
    if hasattr(booking, 'provider_earning'):
        print(f"Earnings record exists: YES")
        earning = booking.provider_earning
        print(f"Gross: ₹{earning.gross_amount}, Net: ₹{earning.net_amount}")
    else:
        print("Earnings record exists: NO")
        
        # Try to create earnings if payment exists and is completed
        if payment and payment.status == 'completed':
            print("\n>>> Payment is paid but no earnings record. This is the issue!")
            print(">>> Creating earnings record now...")
            
            from decimal import Decimal
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
            print(f">>> Created earnings record: ₹{net_amount} net amount")

print("\n\n=== SUMMARY ===")
total_earnings = ProviderEarnings.objects.all()
print(f"Total earnings records: {total_earnings.count()}")
if total_earnings.exists():
    from django.db.models import Sum
    total = total_earnings.aggregate(Sum('net_amount'))['net_amount__sum']
    pending = total_earnings.filter(payout_status='pending').aggregate(Sum('net_amount'))['net_amount__sum'] or 0
    print(f"Total net earnings: ₹{total}")
    print(f"Pending payout: ₹{pending}")
