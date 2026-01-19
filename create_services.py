"""
Create services and providers for all Kerala districts
Run: python manage.py shell < create_services.py
"""
import os
import django
from decimal import Decimal
from django.contrib.auth.models import User
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'homeserve.settings')
django.setup()

from services.models import ServiceProvider, Service, ServiceCategory

print("🛠️ Creating comprehensive services database...")

# Create categories first
categories_data = [
    ('Plumbing', 'Pipes, faucets, and drainage services'),
    ('Electrical', 'Wiring, fixtures, and electrical repairs'),
    ('Cleaning', 'Home and office cleaning services'),
    ('Carpentry', 'Furniture and woodwork services'),
    ('Painting', 'Interior and exterior painting'),
    ('AC Repair', 'Air conditioning installation and repair'),
    ('Appliance Repair', 'Washing machine, refrigerator, and appliance repairs'),
    ('Pest Control', 'Termite and pest control services'),
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

# Kerala districts
kerala_districts = [
    'Thiruvananthapuram', 'Kollam', 'Pathanamthitta', 'Alappuzha',
    'Kottayam', 'Idukki', 'Ernakulam', 'Thrissur', 'Palakkad',
    'Malappuram', 'Kozhikode', 'Wayanad', 'Kannur', 'Kasaragod'
]

# Provider data for different districts
providers_data = [
    ('Kerala Plumbing Experts', 'Ernakulam', 'Kochi', '682001', 10, 'Expert plumbing services'),
    ('Smart Electricians', 'Thiruvananthapuram', 'Trivandrum', '695001', 8, 'Licensed electrical services'),
    ('Home Cleaning Pro', 'Kozhikode', 'Kozhikode', '673001', 5, 'Professional cleaning'),
    ('AC Care Kerala', 'Thrissur', 'Thrissur', '680001', 12, 'AC installation and repair'),
    ('Prime Carpenters', 'Kottayam', 'Kottayam', '686001', 7, 'Custom furniture and repairs'),
    ('Color Masters Painting', 'Kollam', 'Kollam', '691001', 6, 'Interior and exterior painting'),
    ('Fix It Appliances', 'Palakkad', 'Palakkad', '678001', 9, 'All appliance repairs'),
    ('SafeHome Pest Control', 'Malappuram', 'Malappuram', '676001', 4, 'Pest control solutions'),
]

# Services by category
services_by_category = {
    'Plumbing': [
        ('Pipe Repair & Replacement', 500, 'Fix leaking pipes and faucets'),
        ('Drain Cleaning', 800, 'Clear blocked drains and sewers'),
        ('Bathroom Fitting', 2000, 'Install bathroom fixtures'),
        ('Water Heater Installation', 1500, 'Install and repair water heaters'),
        ('Toilet Repair', 600, 'Fix toilet issues'),
    ],
    'Electrical': [
        ('Wiring Repair', 1000, 'Fix electrical wiring issues'),
        ('Fan Installation', 300, 'Install ceiling and wall fans'),
        ('Light Fixture Setup', 400, 'Install lights and fixtures'),
        ('Circuit Breaker Repair', 800, 'Fix electrical panels'),
        ('Switch & Socket Installation', 250, 'Install switches and sockets'),
    ],
    'Cleaning': [
        ('Deep Home Cleaning', 1200, 'Complete home cleaning service'),
        ('Kitchen Cleaning', 600, 'Deep clean kitchen and appliances'),
        ('Bathroom Cleaning', 400, 'Thorough bathroom cleaning'),
        ('Window Cleaning', 500, 'Clean all windows'),
        ('Office Cleaning', 1500, 'Professional office cleaning'),
    ],
    'AC Repair': [
        ('AC Installation', 2500, 'Install new air conditioner'),
        ('AC Servicing', 800, 'Regular AC maintenance'),
        ('AC Gas Refill', 1200, 'Refill AC refrigerant gas'),
        ('AC Repair', 1500, 'Fix AC problems'),
    ],
    'Carpentry': [
        ('Custom Furniture', 5000, 'Make custom furniture'),
        ('Furniture Repair', 800, 'Repair damaged furniture'),
        ('Door & Window Repair', 1000, 'Fix doors and windows'),
        ('Kitchen Cabinet Installation', 3000, 'Install kitchen cabinets'),
    ],
    'Painting': [
        ('Interior Painting', 2500, 'Paint interior walls'),
        ('Exterior Painting', 3000, 'Paint exterior walls'),
        ('Texture Painting', 3500, 'Designer texture painting'),
        ('Wood Polishing', 1500, 'Polish wooden furniture'),
    ],
    'Appliance Repair': [
        ('Washing Machine Repair', 800, 'Fix washing machine issues'),
        ('Refrigerator Repair', 1000, 'Repair refrigerator'),
        ('Microwave Repair', 600, 'Fix microwave oven'),
        ('TV Repair', 1200, 'Repair television'),
    ],
    'Pest Control': [
        ('Termite Control', 2000, 'Eliminate termites'),
        ('General Pest Control', 1500, 'Control cockroaches, ants, etc.'),
        ('Rodent Control', 1800, 'Remove rats and mice'),
        ('Bed Bug Treatment', 2500, 'Eliminate bed bugs'),
    ],
}

# Create providers and their services
print("\n🏢 Creating providers across Kerala districts...")

provider_count = 0
service_count = 0

for business_name, district, city, pincode, exp, bio in providers_data:
    # Find or create a user for this provider
    username = business_name.lower().replace(' ', '_')[:30]
    user, user_created = User.objects.get_or_create(
        username=username,
        defaults={
            'email': f'{username}@homeserve.com',
            'first_name': business_name.split()[0],
            'last_name': 'Services'
        }
    )
    if user_created:
        user.set_password('password123')
        user.save()
    
    # Create provider profile
    provider, prov_created = ServiceProvider.objects.get_or_create(
        user=user,
        defaults={
            'business_name': business_name,
            'contact_number': f'9876543{provider_count:03d}',
            'email': user.email,
            'address': f'{provider_count+100} Main Road',
            'city': district,  # Using district as city
            'state': 'Kerala',
            'pincode': pincode,
            'experience_years': exp,
            'bio': bio,
            'verification_status': 'verified',
            'verified_at': timezone.now(),
            'is_available': True,
            'average_rating': Decimal('4.5'),
        }
    )
    
    if prov_created:
        provider_count += 1
        print(f"   ✓ Created provider: {business_name} in {district}")
    
    # Assign services based on provider specialty
    if 'Plumbing' in business_name:
        category_name = 'Plumbing'
    elif 'Electric' in business_name:
        category_name = 'Electrical'
    elif 'Cleaning' in business_name:
        category_name = 'Cleaning'
    elif 'AC' in business_name:
        category_name = 'AC Repair'
    elif 'Carpenter' in business_name:
        category_name = 'Carpentry'
    elif 'Painting' in business_name:
        category_name = 'Painting'
    elif 'Appliance' in business_name:
        category_name = 'Appliance Repair'
    elif 'Pest' in business_name:
        category_name = 'Pest Control'
    else:
        category_name = 'Plumbing'  # default
    
    # Create services for this provider
    if category_name in services_by_category:
        for service_title, price, desc in services_by_category[category_name]:
            service, svc_created = Service.objects.get_or_create(
                provider=provider,
                title=service_title,
                defaults={
                    'category': categories.get(category_name),
                    'description': desc,
                    'price': Decimal(price),
                    'duration_minutes': 60,
                    'is_active': True,
                    'approval_status': 'approved',
                }
            )
            if svc_created:
                service_count += 1

print(f"\n✅ Created {provider_count} providers and {service_count} services successfully!")
print(f"Total providers in database: {ServiceProvider.objects.count()}")
print(f"Total services in database: {Service.objects.count()}")
print(f"Total categories: {ServiceCategory.objects.filter(is_active=True).count()}")
print(f"\nProviders are spread across: {', '.join(kerala_districts[:8])}, and more!")
