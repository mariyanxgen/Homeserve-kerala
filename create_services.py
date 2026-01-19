"""
Create services for all providers
Run: python manage.py shell < create_services.py
"""
import os
import django
from decimal import Decimal

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'homeserve.settings')
django.setup()

from services.models import ServiceProvider, Service, ServiceCategory

print("🛠️ Creating services...")

# Create categories first
categories_data = [
    ('Plumbing', 'Pipes, faucets, and drainage services'),
    ('Electrical', 'Wiring, fixtures, and electrical repairs'),
    ('Cleaning', 'Home and office cleaning services'),
    ('Carpentry', 'Furniture and woodwork services'),
    ('Painting', 'Interior and exterior painting'),
    ('AC Repair', 'Air conditioning installation and repair'),
]

categories = {}
for name, desc in categories_data:
    cat, created = ServiceCategory.objects.get_or_create(
        name=name,
        defaults={'description': desc, 'is_active': True}
    )
    if not created and not cat.is_active:
        cat.is_active = True
        cat.save()
    categories[name] = cat
    if created:
        print(f"   ✓ Created category: {name}")

# Services data for each provider
services_data = {
    'Kerala Plumbing Experts': [
        ('Pipe Repair', 'Plumbing', 500, 'Fix leaking pipes and faucets'),
        ('Drain Cleaning', 'Plumbing', 800, 'Clear blocked drains'),
        ('Bathroom Fitting', 'Plumbing', 2000, 'Install bathroom fixtures'),
        ('Water Heater Installation', 'Plumbing', 1500, 'Install and repair water heaters'),
    ],
    'Smart Electricians': [
        ('Wiring Repair', 'Electrical', 1000, 'Fix electrical wiring issues'),
        ('Fan Installation', 'Electrical', 300, 'Install ceiling fans'),
        ('Light Fixture Setup', 'Electrical', 400, 'Install lights and fixtures'),
        ('Circuit Breaker Repair', 'Electrical', 800, 'Fix electrical panels'),
    ],
    'Home Cleaning Pro': [
        ('Deep Home Cleaning', 'Cleaning', 1200, 'Complete home cleaning service'),
        ('Kitchen Cleaning', 'Cleaning', 600, 'Deep clean kitchen and appliances'),
        ('Bathroom Cleaning', 'Cleaning', 400, 'Thorough bathroom cleaning'),
        ('Window Cleaning', 'Cleaning', 500, 'Clean all windows'),
    ],
}

# Create services for each provider
providers = ServiceProvider.objects.all()
service_count = 0

for provider in providers:
    if provider.business_name in services_data:
        for service_name, category_name, price, desc in services_data[provider.business_name]:
            service, created = Service.objects.get_or_create(
                provider=provider,
                title=service_name,
                defaults={
                    'category': categories.get(category_name),
                    'description': desc,
                    'price': Decimal(price),
                    'duration_minutes': 60,
                    'is_active': True,
                    'approval_status': 'approved',
                }
            )
            if created:
                service_count += 1
                print(f"   ✓ Created: {service_name} for {provider.business_name} - ₹{price}")

print(f"\n✅ Created {service_count} services successfully!")
print(f"Total services in database: {Service.objects.count()}")
