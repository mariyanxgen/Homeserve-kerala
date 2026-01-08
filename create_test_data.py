# Quick Test Data Creation Script
# Run: python manage.py shell < create_test_data.py

from django.contrib.auth.models import User
from services.models import (
    ServiceCategory, ServiceProvider, Service,
    Booking, Review
)
from datetime import date, time, timedelta
from django.utils import timezone

print("🚀 Creating test data for HomeServe...")

# Create Service Categories
print("\n📂 Creating service categories...")
categories_data = [
    {"name": "Plumbing", "description": "Professional plumbing services for homes and offices", "icon": "🔧"},
    {"name": "Electrical Work", "description": "Licensed electricians for all electrical needs", "icon": "⚡"},
    {"name": "Home Cleaning", "description": "Professional cleaning services for residential spaces", "icon": "🧹"},
    {"name": "AC Repair", "description": "Air conditioning installation and repair services", "icon": "❄️"},
    {"name": "Carpentry", "description": "Custom woodwork and furniture repair", "icon": "🪚"},
]

categories = {}
for cat_data in categories_data:
    cat, created = ServiceCategory.objects.get_or_create(
        name=cat_data["name"],
        defaults={
            "description": cat_data["description"],
            "icon": cat_data["icon"],
            "is_active": True
        }
    )
    categories[cat_data["name"]] = cat
    print(f"  ✓ {cat.name}")

# Create Users for Providers
print("\n👤 Creating provider users...")
providers_data = [
    {
        "username": "john_plumber",
        "email": "john@plumbing.com",
        "first_name": "John",
        "last_name": "Smith",
        "business_name": "Smith Plumbing Services",
        "contact": "+1234567890",
        "city": "New York",
        "state": "NY",
        "pincode": "10001",
        "experience": 5,
        "bio": "Professional plumber with 5 years of experience in residential and commercial plumbing",
    },
    {
        "username": "sarah_electric",
        "email": "sarah@electric.com",
        "first_name": "Sarah",
        "last_name": "Johnson",
        "business_name": "Johnson Electricals",
        "contact": "+1234567891",
        "city": "Los Angeles",
        "state": "CA",
        "pincode": "90001",
        "experience": 8,
        "bio": "Licensed electrician specializing in home wiring and repairs",
    },
    {
        "username": "mike_cleaner",
        "email": "mike@cleaning.com",
        "first_name": "Mike",
        "last_name": "Wilson",
        "business_name": "Wilson Cleaning Co.",
        "contact": "+1234567892",
        "city": "Chicago",
        "state": "IL",
        "pincode": "60601",
        "experience": 3,
        "bio": "Eco-friendly cleaning services for homes and offices",
    },
]

providers = {}
for prov_data in providers_data:
    user, created = User.objects.get_or_create(
        username=prov_data["username"],
        defaults={
            "email": prov_data["email"],
            "first_name": prov_data["first_name"],
            "last_name": prov_data["last_name"],
        }
    )
    if created:
        user.set_password("test123")
        user.save()
    
    provider, created = ServiceProvider.objects.get_or_create(
        user=user,
        defaults={
            "business_name": prov_data["business_name"],
            "contact_number": prov_data["contact"],
            "email": prov_data["email"],
            "address": f"{prov_data['pincode']} Main Street",
            "city": prov_data["city"],
            "state": prov_data["state"],
            "pincode": prov_data["pincode"],
            "experience_years": prov_data["experience"],
            "bio": prov_data["bio"],
            "verification_status": "verified" if prov_data["username"] != "mike_cleaner" else "pending",
            "verified_at": timezone.now() if prov_data["username"] != "mike_cleaner" else None,
            "is_available": True,
            "available_from": time(9, 0),
            "available_to": time(18, 0),
        }
    )
    providers[prov_data["business_name"]] = provider
    print(f"  ✓ {provider.business_name} ({user.username})")

# Create Services
print("\n🛠️ Creating services...")
services_data = [
    {
        "provider": "Smith Plumbing Services",
        "category": "Plumbing",
        "title": "Leak Repair & Pipe Fixing",
        "description": "Expert repair of leaking pipes, faucets, and drainage systems",
        "pricing_type": "fixed",
        "price": 75.00,
        "duration": 90,
        "emergency": True,
    },
    {
        "provider": "Smith Plumbing Services",
        "category": "Plumbing",
        "title": "Bathroom Installation",
        "description": "Complete bathroom plumbing installation including fixtures",
        "pricing_type": "negotiable",
        "price": 500.00,
        "duration": 480,
        "emergency": False,
    },
    {
        "provider": "Johnson Electricals",
        "category": "Electrical Work",
        "title": "Home Wiring & Rewiring",
        "description": "Complete electrical wiring services for homes",
        "pricing_type": "hourly",
        "price": 50.00,
        "duration": 60,
        "emergency": True,
    },
    {
        "provider": "Johnson Electricals",
        "category": "Electrical Work",
        "title": "Light Fixture Installation",
        "description": "Installation of ceiling fans, chandeliers, and light fixtures",
        "pricing_type": "fixed",
        "price": 45.00,
        "duration": 45,
        "emergency": False,
    },
    {
        "provider": "Wilson Cleaning Co.",
        "category": "Home Cleaning",
        "title": "Deep House Cleaning",
        "description": "Comprehensive cleaning service for entire house",
        "pricing_type": "fixed",
        "price": 150.00,
        "duration": 240,
        "emergency": False,
    },
]

services = {}
for serv_data in services_data:
    service, created = Service.objects.get_or_create(
        provider=providers[serv_data["provider"]],
        title=serv_data["title"],
        defaults={
            "category": categories[serv_data["category"]],
            "description": serv_data["description"],
            "pricing_type": serv_data["pricing_type"],
            "price": serv_data["price"],
            "duration_minutes": serv_data["duration"],
            "is_active": True,
            "is_emergency_available": serv_data["emergency"],
        }
    )
    services[serv_data["title"]] = service
    print(f"  ✓ {service.title} - ${service.price}")

# Create Customer User
print("\n👥 Creating customer user...")
customer, created = User.objects.get_or_create(
    username="customer1",
    defaults={
        "email": "alice@customer.com",
        "first_name": "Alice",
        "last_name": "Brown",
    }
)
if created:
    customer.set_password("test123")
    customer.save()
print(f"  ✓ {customer.username} ({customer.first_name} {customer.last_name})")

# Create Sample Bookings
print("\n📅 Creating bookings...")
bookings_data = [
    {
        "service": "Leak Repair & Pipe Fixing",
        "date": date.today() + timedelta(days=2),
        "time": time(10, 0),
        "status": "confirmed",
        "payment": "paid",
        "notes": "Kitchen sink is leaking badly",
    },
    {
        "service": "Deep House Cleaning",
        "date": date.today() + timedelta(days=5),
        "time": time(9, 0),
        "status": "pending",
        "payment": "pending",
        "notes": "Need deep cleaning before guests arrive",
    },
    {
        "service": "Home Wiring & Rewiring",
        "date": date.today() + timedelta(days=7),
        "time": time(11, 0),
        "status": "pending",
        "payment": "pending",
        "notes": "Need to rewire entire second floor",
    },
]

for book_data in bookings_data:
    service = services[book_data["service"]]
    booking, created = Booking.objects.get_or_create(
        customer=customer,
        service=service,
        booking_date=book_data["date"],
        defaults={
            "provider": service.provider,
            "booking_time": book_data["time"],
            "address": "321 Customer Street, Apt 5B",
            "city": "New York",
            "pincode": "10002",
            "customer_notes": book_data["notes"],
            "estimated_duration": service.duration_minutes,
            "status": book_data["status"],
            "total_amount": service.price,
            "payment_status": book_data["payment"],
            "confirmed_at": timezone.now() if book_data["status"] == "confirmed" else None,
        }
    )
    print(f"  ✓ Booking #{booking.id} - {service.title} on {book_data['date']}")

print("\n✅ Test data created successfully!")
print("\n📊 Summary:")
print(f"  - {ServiceCategory.objects.count()} categories")
print(f"  - {ServiceProvider.objects.count()} providers")
print(f"  - {Service.objects.count()} services")
print(f"  - {Booking.objects.count()} bookings")
print("\n🔐 Login Credentials:")
print("  Admin: Create using 'python manage.py createsuperuser'")
print("  Provider 1: john_plumber / test123")
print("  Provider 2: sarah_electric / test123")
print("  Provider 3: mike_cleaner / test123")
print("  Customer: customer1 / test123")
print("\n🌐 Access Points:")
print("  Admin: http://127.0.0.1:8000/admin/")
print("  API: http://127.0.0.1:8000/api/")
