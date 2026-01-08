import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'homeserve.settings')
django.setup()

from services.models import Booking, Payment, ProviderEarnings
from decimal import Decimal
from django.utils import timezone

# Get booking #6
booking = Booking.objects.get(id=6)
print(f"Booking #{booking.id}: {booking.service.title}")
print(f"Customer: {booking.customer_name}")
print(f"Amount: ₹{booking.service.price}")
print(f"Status: {booking.status}")
print()

# Create payment
commission_pct = Decimal('15.00')
provider_amt = booking.service.price * (Decimal('100.00') - commission_pct) / Decimal('100.00')

payment = Payment.objects.create(
    booking=booking,
    user=booking.user,
    amount=booking.service.price,
    payment_method='online',
    status='completed',
    transaction_id=f'TXN{booking.id}AUTO',
    platform_commission=commission_pct,
    provider_amount=provider_amt,
    paid_at=booking.completed_at or timezone.now()
)
print(f"✓ Created Payment: ₹{payment.amount} (Status: {payment.status})")

# Create earnings
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

print(f"\n✓ Created Earnings:")
print(f"  Gross Amount: ₹{earning.gross_amount}")
print(f"  Commission (10%): -₹{earning.commission_amount}")
print(f"  Net Amount: ₹{earning.net_amount}")

print("\n" + "="*60)
print("SUMMARY:")
all_earnings = ProviderEarnings.objects.filter(provider=booking.provider)
from django.db.models import Sum
total = all_earnings.aggregate(total=Sum('net_amount'))['total'] or 0
pending = all_earnings.filter(payout_status='pending').aggregate(total=Sum('net_amount'))['total'] or 0
print(f"Total earnings for provider: ₹{total}")
print(f"Pending payout: ₹{pending}")
print(f"\nRefresh the earnings page to see ₹{total}!")
