import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'homeserve.settings')
django.setup()

from services.models import Booking, Payment, ProviderEarnings
from decimal import Decimal

# Get booking #5
booking = Booking.objects.get(id=5)
print(f"Booking #{booking.id}")
print(f"Customer: {booking.customer_name}")
print(f"Service: {booking.service.title}")
print(f"Provider: {booking.provider.business_name}")
print(f"Status: {booking.status}")
print(f"Service Price: ₹{booking.service.price}")

# Check if payment exists
try:
    payment = Payment.objects.get(booking=booking)
    print(f"\nPayment exists: YES")
    print(f"Amount: ₹{payment.amount}")
    print(f"Status: {payment.status}")
except Payment.DoesNotExist:
    print(f"\nPayment exists: NO - Creating payment now...")
    
    # Create payment record
    payment = Payment.objects.create(
        booking=booking,
        user=booking.user,
        amount=booking.service.price,
        payment_method='cash',  # or whatever method was used
        status='completed',
        transaction_id=f'TXN{booking.id}',
        platform_commission=Decimal('10.00'),
        provider_amount=booking.service.price * Decimal('0.90')
    )
    print(f"Created payment: ₹{payment.amount} (Status: {payment.status})")
    
    # Now create earnings record
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
    print(f"Created earnings record: ₹{net_amount} net amount (Gross: ₹{gross_amount}, Commission: ₹{commission_amount})")

print("\n=== VERIFICATION ===")
all_earnings = ProviderEarnings.objects.filter(provider=booking.provider)
total = sum(e.net_amount for e in all_earnings)
print(f"Total earnings for {booking.provider.business_name}: ₹{total}")
print(f"Number of earnings records: {all_earnings.count()}")
