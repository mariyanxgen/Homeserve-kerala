import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'homeserve.settings')
django.setup()

from services.models import Booking, Payment, ProviderEarnings
from decimal import Decimal
from django.utils import timezone

# Get the completed booking
booking = Booking.objects.get(id=5)
print(f"Booking #{booking.id}: {booking.service.title}")
print(f"Customer: {booking.customer_name}")
print(f"Amount: ₹{booking.service.price}")
print(f"Status: {booking.status}")
print()

# Create payment record
commission_pct = Decimal('15.00')  # Platform commission
provider_amt = booking.service.price * (Decimal('100.00') - commission_pct) / Decimal('100.00')

payment, created = Payment.objects.get_or_create(
    booking=booking,
    defaults={
        'user': booking.user,
        'amount': booking.service.price,
        'payment_method': 'online',
        'status': 'completed',
        'transaction_id': f'TXN{booking.id}AUTO',
        'platform_commission': commission_pct,
        'provider_amount': provider_amt,
        'paid_at': booking.completed_at or timezone.now()
    }
)

if created:
    print(f"✓ Created Payment: ₹{payment.amount} - Status: {payment.status}")
else:
    print(f"✓ Payment already exists: ₹{payment.amount} - Status: {payment.status}")

print()

# Create earnings record
if not hasattr(booking, 'provider_earning'):
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
    
    print(f"✓ Created Earnings Record:")
    print(f"  - Gross Amount: ₹{earning.gross_amount}")
    print(f"  - Commission (10%): -₹{earning.commission_amount}")
    print(f"  - Net Amount: ₹{earning.net_amount}")
    print(f"  - Payout Status: {earning.payout_status}")
else:
    print("✓ Earnings already exist for this booking")

print()
print("=" * 60)
print("Summary:")
from django.db.models import Sum
total = ProviderEarnings.objects.filter(provider=booking.provider).aggregate(total=Sum('net_amount'))['total'] or 0
print(f"Provider total earnings: ₹{total}")
print("Refresh the earnings page to see the updated amounts!")
