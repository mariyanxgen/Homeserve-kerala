"""
Script to populate database with sample data for all new features
Run: python manage.py shell < populate_all_features.py
"""

import os
import django
from decimal import Decimal
from datetime import datetime, timedelta, time, date
from django.utils import timezone
from django.contrib.auth.models import User

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'homeserve.settings')
django.setup()

from services.models import (
    ServiceProvider, Service, Booking, ServiceCategory,
    # Payment & Wallet
    Wallet, Payment, Transaction,
    # Messaging
    Message,
    # Provider Analytics
    ProviderEarnings, ProviderStats,
    # Promotions
    Coupon, ServicePackage, Referral, LoyaltyPoints,
    # Customer Features
    FavoriteProvider, CustomerAddress, Notification,
    # Verification
    ProviderDocument, ProviderInsurance,
    # Advanced Booking
    RecurringBooking, BookingExtension,
    # Scheduling
    ProviderAvailability, ProviderLeave
)

print("🚀 Starting database population...")

# ==================== CREATE USERS ====================
print("\n👥 Creating users...")

# Create customers
customers = []
customer_data = [
    ('john_doe', 'john@example.com', 'John', 'Doe'),
    ('jane_smith', 'jane@example.com', 'Jane', 'Smith'),
    ('mike_wilson', 'mike@example.com', 'Mike', 'Wilson'),
    ('sarah_jones', 'sarah@example.com', 'Sarah', 'Jones'),
    ('david_brown', 'david@example.com', 'David', 'Brown'),
]

for username, email, first, last in customer_data:
    user, created = User.objects.get_or_create(
        username=username,
        defaults={'email': email, 'first_name': first, 'last_name': last}
    )
    if created:
        user.set_password('password123')
        user.save()
        print(f"   ✓ Created customer: {username}")
    customers.append(user)

# Create provider users
providers_data = [
    ('provider1', 'provider1@homeserve.com', 'Rajan', 'Kumar'),
    ('provider2', 'provider2@homeserve.com', 'Suresh', 'Menon'),
    ('provider3', 'provider3@homeserve.com', 'Anjali', 'Nair'),
]

provider_users = []
for username, email, first, last in providers_data:
    user, created = User.objects.get_or_create(
        username=username,
        defaults={'email': email, 'first_name': first, 'last_name': last}
    )
    if created:
        user.set_password('password123')
        user.save()
        print(f"   ✓ Created provider user: {username}")
    provider_users.append(user)

# ==================== CREATE SERVICE PROVIDERS ====================
print("\n🔧 Creating service providers...")

provider_profiles = []
provider_info = [
    ('Kerala Plumbing Experts', 'Kochi', 'Kerala', '682001', 10, 'Expert plumbing services with 10 years experience'),
    ('Smart Electricians', 'Thiruvananthapuram', 'Kerala', '695001', 8, 'Licensed electrical services'),
    ('Home Cleaning Pro', 'Kozhikode', 'Kerala', '673001', 5, 'Professional home cleaning services'),
]

for i, (business, city, state, pincode, exp, bio) in enumerate(provider_info):
    if i < len(provider_users):
        provider, created = ServiceProvider.objects.get_or_create(
            user=provider_users[i],
            defaults={
                'business_name': business,
                'contact_number': f'987654321{i}',
                'email': provider_users[i].email,
                'address': f'{i+100} MG Road',
                'city': city,
                'state': state,
                'pincode': pincode,
                'experience_years': exp,
                'bio': bio,
                'verification_status': 'verified',
                'verified_at': timezone.now(),
                'is_available': True,
                'average_rating': Decimal('4.5'),
            }
        )
        if created:
            print(f"   ✓ Created provider: {business}")
        provider_profiles.append(provider)

# ==================== CREATE WALLETS ====================
print("\n💰 Creating wallets...")

for user in customers + provider_users:
    wallet, created = Wallet.objects.get_or_create(
        user=user,
        defaults={'balance': Decimal('500.00'), 'is_active': True}
    )
    if created:
        print(f"   ✓ Created wallet for {user.username} with ₹500")

# ==================== CREATE LOYALTY POINTS ====================
print("\n⭐ Creating loyalty points...")

for customer in customers:
    points, created = LoyaltyPoints.objects.get_or_create(
        user=customer,
        defaults={
            'points': 1500,
            'tier': 'silver',
            'total_earned': 2000,
            'total_redeemed': 500,
        }
    )
    if created:
        print(f"   ✓ Created loyalty points for {customer.username}: {points.points} points ({points.tier})")

# ==================== CREATE CUSTOMER ADDRESSES ====================
print("\n🏠 Creating customer addresses...")

addresses_data = [
    ('Home', 'home', 'Panampilly Nagar', 'Kochi', 'Kerala', '682036'),
    ('Office', 'work', 'Infopark Campus', 'Kochi', 'Kerala', '682042'),
    ('Parents House', 'other', 'Vytilla', 'Kochi', 'Kerala', '682019'),
]

for customer in customers[:2]:  # Add addresses for first 2 customers
    for i, (label, addr_type, area, city, state, pincode) in enumerate(addresses_data[:2]):
        address, created = CustomerAddress.objects.get_or_create(
            customer=customer,
            label=label,
            defaults={
                'address_type': addr_type,
                'address_line1': f'{(i+1)*10} Main Street',
                'address_line2': area,
                'city': city,
                'state': state,
                'pincode': pincode,
                'is_default': (i == 0),
            }
        )
        if created:
            print(f"   ✓ Created address '{label}' for {customer.username}")

# ==================== CREATE FAVORITE PROVIDERS ====================
print("\n❤️ Creating favorite providers...")

for customer in customers[:3]:
    for provider in provider_profiles[:2]:
        fav, created = FavoriteProvider.objects.get_or_create(
            customer=customer,
            provider=provider
        )
        if created:
            print(f"   ✓ {customer.username} favorited {provider.business_name}")

# ==================== CREATE COUPONS ====================
print("\n🎫 Creating coupons...")

coupons_data = [
    ('FIRST50', 'percentage', 50, 500, 100, 'First booking 50% off'),
    ('SAVE100', 'fixed', 100, None, 500, 'Flat ₹100 off on orders above ₹500'),
    ('WELCOME20', 'percentage', 20, 200, 300, 'Welcome offer - 20% off'),
    ('NEWYEAR2026', 'percentage', 30, 500, 1000, 'New Year Special - 30% off'),
]

categories = ServiceCategory.objects.all()

for code, ctype, value, max_disc, min_order, desc in coupons_data:
    coupon, created = Coupon.objects.get_or_create(
        code=code,
        defaults={
            'description': desc,
            'coupon_type': ctype,
            'discount_value': Decimal(value),
            'max_discount': Decimal(max_disc) if max_disc else None,
            'min_order_value': Decimal(min_order),
            'usage_limit': 100,
            'used_count': 15,
            'per_user_limit': 1,
            'valid_from': timezone.now() - timedelta(days=10),
            'valid_to': timezone.now() + timedelta(days=30),
            'is_active': True,
        }
    )
    if created:
        if categories.exists():
            coupon.applicable_categories.add(categories.first())
        print(f"   ✓ Created coupon: {code}")

# ==================== CREATE SERVICE PACKAGES ====================
print("\n📦 Creating service packages...")

for provider in provider_profiles:
    services = Service.objects.filter(provider=provider)[:3]
    if services.count() >= 2:
        package, created = ServicePackage.objects.get_or_create(
            provider=provider,
            title=f'{provider.business_name} Monthly Package',
            defaults={
                'description': 'Complete home maintenance package with 3 services',
                'regular_price': Decimal('3000.00'),
                'package_price': Decimal('2400.00'),
                'savings': Decimal('600.00'),
                'duration_months': 1,
                'is_active': True,
            }
        )
        if created:
            package.services.set(services)
            print(f"   ✓ Created package for {provider.business_name}")

# ==================== CREATE REFERRALS ====================
print("\n🔗 Creating referrals...")

if len(customers) >= 2:
    for i in range(min(2, len(customers) - 1)):
        referral, created = Referral.objects.get_or_create(
            referrer=customers[i],
            referred=customers[i+1],
            defaults={
                'referral_code': f'REF{customers[i].id}{customers[i+1].id}',
                'referrer_reward': Decimal('100.00'),
                'referred_reward': Decimal('50.00'),
                'is_completed': True,
                'completed_at': timezone.now(),
                'rewards_credited': True,
            }
        )
        if created:
            print(f"   ✓ {customers[i].username} referred {customers[i+1].username}")

# ==================== CREATE PROVIDER DOCUMENTS ====================
print("\n📄 Creating provider documents...")

doc_types = ['id_proof', 'business_license', 'certificate']
for provider in provider_profiles:
    for doc_type in doc_types[:2]:
        doc, created = ProviderDocument.objects.get_or_create(
            provider=provider,
            document_type=doc_type,
            defaults={
                'document_number': f'{doc_type.upper()}{provider.id}123456',
                'verification_status': 'verified',
                'verified_at': timezone.now(),
                'expires_at': date.today() + timedelta(days=365),
            }
        )
        if created:
            print(f"   ✓ Created {doc_type} for {provider.business_name}")

# ==================== CREATE PROVIDER INSURANCE ====================
print("\n🛡️ Creating provider insurance...")

for provider in provider_profiles:
    insurance, created = ProviderInsurance.objects.get_or_create(
        provider=provider,
        defaults={
            'insurance_company': 'Kerala General Insurance',
            'policy_number': f'POL{provider.id}2026',
            'coverage_amount': Decimal('1000000.00'),
            'valid_from': date.today(),
            'valid_to': date.today() + timedelta(days=365),
            'is_active': True,
        }
    )
    if created:
        print(f"   ✓ Created insurance for {provider.business_name}")

# ==================== CREATE PROVIDER AVAILABILITY ====================
print("\n📅 Creating provider availability schedules...")

for provider in provider_profiles:
    for weekday in range(6):  # Monday to Saturday
        avail, created = ProviderAvailability.objects.get_or_create(
            provider=provider,
            weekday=weekday,
            defaults={
                'is_available': True,
                'start_time': time(9, 0),
                'end_time': time(18, 0),
                'break_start': time(13, 0),
                'break_end': time(14, 0),
            }
        )
        if created and weekday == 0:  # Print once per provider
            print(f"   ✓ Created weekly schedule for {provider.business_name}")

# ==================== CREATE BOOKINGS WITH PAYMENTS ====================
print("\n📋 Creating bookings with payments...")

services = Service.objects.all()
if services.exists():
    for i, customer in enumerate(customers[:3]):
        service = services[i % services.count()]
        
        # Create booking
        booking, created = Booking.objects.get_or_create(
            user=customer,
            service=service,
            provider=service.provider,
            defaults={
                'customer_name': customer.get_full_name() or customer.username,
                'customer_email': customer.email,
                'customer_phone': f'987654{i:04d}',
                'customer_address': f'{i+1} Customer Street, Kochi',
                'booking_date': date.today() + timedelta(days=i+1),
                'booking_time': time(10, 0),
                'notes': f'Booking by {customer.username}',
                'status': 'completed',
                'total_amount': service.price,
                'is_emergency': False,
                'confirmed_at': timezone.now(),
                'completed_at': timezone.now(),
            }
        )
        
        if created:
            print(f"   ✓ Created booking #{booking.id} for {customer.username}")
            
            # Create payment
            payment, p_created = Payment.objects.get_or_create(
                booking=booking,
                user=customer,
                defaults={
                    'amount': booking.total_amount,
                    'payment_method': 'upi',
                    'status': 'completed',
                    'transaction_id': f'TXN{booking.id}2026{i:04d}',
                    'gateway_order_id': f'ORDER{booking.id}',
                    'gateway_payment_id': f'PAY{booking.id}',
                    'platform_commission': Decimal('15.00'),
                    'provider_amount': booking.total_amount * Decimal('0.85'),
                    'paid_at': timezone.now(),
                }
            )
            
            if p_created:
                payment.calculate_provider_amount()
                print(f"   ✓ Created payment ₹{payment.amount} for booking #{booking.id}")
                
                # Create provider earnings
                earning, e_created = ProviderEarnings.objects.get_or_create(
                    provider=service.provider,
                    booking=booking,
                    payment=payment,
                    defaults={
                        'gross_amount': payment.amount,
                        'commission_percentage': payment.platform_commission,
                        'commission_amount': payment.amount * payment.platform_commission / 100,
                        'net_amount': payment.provider_amount,
                        'payout_status': 'paid',
                        'paid_at': timezone.now(),
                    }
                )
                if e_created:
                    print(f"   ✓ Created earnings ₹{earning.net_amount} for {service.provider.business_name}")
                
                # Create booking extension
                ext, ext_created = BookingExtension.objects.get_or_create(
                    booking=booking,
                    defaults={
                        'estimated_arrival_time': timezone.now(),
                        'actual_arrival_time': timezone.now() + timedelta(minutes=15),
                        'service_started_at': timezone.now() + timedelta(minutes=20),
                        'service_ended_at': timezone.now() + timedelta(hours=2),
                        'materials_used': 'Standard plumbing materials, pipes, sealant',
                        'work_description': 'Completed the service successfully',
                        'warranty_period_days': 90,
                        'warranty_terms': '3 months warranty on workmanship',
                    }
                )

# ==================== CREATE MESSAGES ====================
print("\n💬 Creating messages...")

bookings = Booking.objects.all()
if bookings.exists():
    for booking in bookings[:3]:
        if booking.user and booking.provider.user:
            # Customer to provider
            msg1, created = Message.objects.get_or_create(
                booking=booking,
                sender=booking.user,
                receiver=booking.provider.user,
                defaults={
                    'message_text': f'Hi, I have booked your service for {booking.booking_date}. Please confirm.',
                    'is_read': True,
                    'read_at': timezone.now(),
                }
            )
            
            # Provider to customer
            msg2, c2 = Message.objects.get_or_create(
                booking=booking,
                sender=booking.provider.user,
                receiver=booking.user,
                defaults={
                    'message_text': f'Thank you for booking! I will be there at {booking.booking_time}.',
                    'is_read': False,
                }
            )
            
            if created:
                print(f"   ✓ Created messages for booking #{booking.id}")

# ==================== CREATE NOTIFICATIONS ====================
print("\n🔔 Creating notifications...")

notification_data = [
    ('booking', 'Booking Confirmed', 'Your booking has been confirmed for {}'),
    ('payment', 'Payment Successful', 'Payment of ₹{} received successfully'),
    ('promotion', 'Special Offer', 'Use code SAVE100 and get ₹100 off'),
    ('system', 'Welcome!', 'Welcome to Kerala HomeServe Pro'),
]

for customer in customers:
    for ntype, title, msg in notification_data[:2]:
        notif, created = Notification.objects.get_or_create(
            user=customer,
            notification_type=ntype,
            title=title,
            defaults={
                'message': msg.format('tomorrow' if '{}' in msg else ''),
                'is_read': False,
            }
        )
        if created and notification_data.index((ntype, title, msg)) == 0:
            print(f"   ✓ Created notifications for {customer.username}")

# ==================== CREATE PROVIDER STATS ====================
print("\n📊 Creating provider stats...")

for provider in provider_profiles:
    for days_ago in range(7):  # Last 7 days
        stat_date = date.today() - timedelta(days=days_ago)
        stat, created = ProviderStats.objects.get_or_create(
            provider=provider,
            date=stat_date,
            defaults={
                'bookings_received': 5,
                'bookings_completed': 4,
                'bookings_cancelled': 1,
                'revenue': Decimal('2000.00'),
                'reviews_received': 3,
                'average_rating_day': Decimal('4.5'),
                'average_response_time': 30,
            }
        )
        if created and days_ago == 0:  # Print once per provider
            print(f"   ✓ Created weekly stats for {provider.business_name}")

# ==================== CREATE RECURRING BOOKINGS ====================
print("\n🔄 Creating recurring bookings...")

if services.exists() and customers:
    service = services.first()
    recurring, created = RecurringBooking.objects.get_or_create(
        customer=customers[0],
        service=service,
        provider=service.provider,
        defaults={
            'frequency': 'weekly',
            'start_date': date.today(),
            'end_date': date.today() + timedelta(days=90),
            'preferred_time': time(10, 0),
            'total_amount': service.price,
            'is_active': True,
            'next_booking_date': date.today() + timedelta(days=7),
        }
    )
    if created:
        print(f"   ✓ Created weekly recurring booking for {customers[0].username}")

# ==================== CREATE TRANSACTIONS ====================
print("\n💳 Creating wallet transactions...")

for customer in customers[:3]:
    wallet = Wallet.objects.filter(user=customer).first()
    if wallet:
        # Credit transaction
        trans1, created = Transaction.objects.get_or_create(
            wallet=wallet,
            amount=Decimal('500.00'),
            transaction_type='credit',
            defaults={
                'description': 'Initial wallet credit',
                'reference_id': f'INIT{customer.id}',
                'balance_after': Decimal('500.00'),
            }
        )
        
        # Debit transaction
        trans2, c2 = Transaction.objects.get_or_create(
            wallet=wallet,
            amount=Decimal('100.00'),
            transaction_type='debit',
            defaults={
                'description': 'Payment for booking',
                'reference_id': f'PAY{customer.id}',
                'balance_after': Decimal('400.00'),
            }
        )
        
        if created:
            print(f"   ✓ Created transactions for {customer.username}")

# ==================== CREATE PROVIDER LEAVES ====================
print("\n🏖️ Creating provider leaves...")

for provider in provider_profiles[:1]:  # Just one provider
    leave, created = ProviderLeave.objects.get_or_create(
        provider=provider,
        leave_type='vacation',
        defaults={
            'start_date': date.today() + timedelta(days=15),
            'end_date': date.today() + timedelta(days=20),
            'reason': 'Family vacation',
            'is_approved': True,
        }
    )
    if created:
        print(f"   ✓ Created vacation leave for {provider.business_name}")

# ==================== SUMMARY ====================
print("\n" + "="*60)
print("✅ DATABASE POPULATION COMPLETED!")
print("="*60)
print(f"\n📊 Summary:")
print(f"   • Users: {User.objects.count()}")
print(f"   • Service Providers: {ServiceProvider.objects.count()}")
print(f"   • Wallets: {Wallet.objects.count()}")
print(f"   • Payments: {Payment.objects.count()}")
print(f"   • Transactions: {Transaction.objects.count()}")
print(f"   • Messages: {Message.objects.count()}")
print(f"   • Bookings: {Booking.objects.count()}")
print(f"   • Coupons: {Coupon.objects.count()}")
print(f"   • Service Packages: {ServicePackage.objects.count()}")
print(f"   • Loyalty Points: {LoyaltyPoints.objects.count()}")
print(f"   • Referrals: {Referral.objects.count()}")
print(f"   • Customer Addresses: {CustomerAddress.objects.count()}")
print(f"   • Notifications: {Notification.objects.count()}")
print(f"   • Provider Documents: {ProviderDocument.objects.count()}")
print(f"   • Provider Insurance: {ProviderInsurance.objects.count()}")
print(f"   • Provider Availability: {ProviderAvailability.objects.count()}")
print(f"   • Provider Stats: {ProviderStats.objects.count()}")
print(f"   • Recurring Bookings: {RecurringBooking.objects.count()}")
print(f"   • Favorite Providers: {FavoriteProvider.objects.count()}")
print(f"   • Provider Earnings: {ProviderEarnings.objects.count()}")
print(f"   • Booking Extensions: {BookingExtension.objects.count()}")

print("\n🎉 All features populated successfully!")
print("\n📝 Test Credentials:")
print("   Customers:")
for u in customer_data[:3]:
    print(f"      • {u[0]} / password123")
print("   Providers:")
for u in providers_data:
    print(f"      • {u[0]} / password123")
print("\n🌐 Access admin panel: http://127.0.0.1:8000/admin/")
print("="*60)
