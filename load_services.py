from services.models import ServiceCategory, ServiceProvider, Service
from django.contrib.auth.models import User

# Get or create categories
categories = {}
category_data = [
    ('Plumbing', 'Professional plumbing services'),
    ('Electrical', 'Electrical installation and repair'),
    ('Cleaning', 'Home and office cleaning services'),
    ('Carpentry', 'Wood work and furniture services'),
    ('Painting', 'Interior and exterior painting'),
    ('AC Repair', 'Air conditioning repair and maintenance'),
    ('Pest Control', 'Professional pest control services'),
    ('Landscaping', 'Garden and lawn maintenance'),
]

for name, desc in category_data:
    cat, _ = ServiceCategory.objects.get_or_create(name=name, defaults={'description': desc})
    categories[name] = cat

# Create providers
providers = []
districts = ['Thiruvananthapuram', 'Kochi', 'Kozhikode', 'Thrissur', 'Kollam']

for i in range(5):
    user, _ = User.objects.get_or_create(
        username=f'provider{i+1}',
        defaults={
            'email': f'provider{i+1}@homeserve.com',
            'first_name': f'Provider{i+1}',
            'last_name': 'Services'
        }
    )
    
    provider, _ = ServiceProvider.objects.get_or_create(
        user=user,
        defaults={
            'business_name': f'{districts[i]} Pro Services',
            'phone': f'98765432{i}0',
            'email': f'contact@provider{i+1}.com',
            'address': f'{i+1}23 Main Road',
            'city': districts[i].split()[0],
            'district': districts[i],
            'pincode': f'68000{i}',
            'is_verified': True,
            'years_of_experience': 5 + i
        }
    )
    providers.append(provider)

# Create services
services = [
    ('Emergency Pipe Leak Repair', 'Plumbing', 'Quick response for urgent pipe leak repairs. Available 24/7.', 800, 60, 'fixed', True),
    ('Bathroom Fittings Installation', 'Plumbing', 'Complete bathroom fitting installation with warranty.', 2500, 180, 'fixed', False),
    ('Water Tank Cleaning', 'Plumbing', 'Thorough water tank cleaning and sanitization service.', 1500, 120, 'fixed', False),
    ('Complete Home Wiring', 'Electrical', 'Full house electrical wiring with modern standards.', 15000, 480, 'negotiable', False),
    ('Fan & Light Installation', 'Electrical', 'Professional installation of ceiling fans and lights.', 500, 45, 'fixed', True),
    ('Electrical Safety Inspection', 'Electrical', 'Comprehensive electrical safety check for your home.', 1200, 90, 'fixed', False),
    ('Deep House Cleaning', 'Cleaning', 'Comprehensive deep cleaning for your entire home.', 3000, 240, 'fixed', False),
    ('Sofa & Carpet Cleaning', 'Cleaning', 'Professional upholstery cleaning using steam technology.', 1800, 120, 'fixed', False),
    ('Kitchen Deep Cleaning', 'Cleaning', 'Specialized kitchen cleaning including chimney and tiles.', 1500, 150, 'fixed', False),
    ('Custom Furniture Making', 'Carpentry', 'Bespoke furniture with design consultation.', 25000, 720, 'negotiable', False),
    ('Door & Window Repair', 'Carpentry', 'Repair of wooden doors and windows.', 800, 90, 'fixed', True),
    ('Modular Kitchen Installation', 'Carpentry', 'Complete modular kitchen with warranty.', 45000, 960, 'negotiable', False),
    ('Interior Wall Painting', 'Painting', 'Complete interior painting with premium paints.', 18, 480, 'hourly', False),
    ('Exterior Wall Painting', 'Painting', 'Weather-resistant exterior painting service.', 22, 600, 'hourly', False),
    ('Texture & Design Painting', 'Painting', 'Decorative texture painting for feature walls.', 3500, 300, 'negotiable', False),
    ('AC Installation & Setup', 'AC Repair', 'Professional air conditioner installation service.', 2500, 120, 'fixed', False),
    ('AC Service & Maintenance', 'AC Repair', 'Regular AC servicing for optimal performance.', 600, 60, 'fixed', True),
    ('AC Gas Refilling', 'AC Repair', 'AC gas refilling and leak detection service.', 1800, 90, 'fixed', True),
    ('General Pest Control', 'Pest Control', 'Treatment for cockroaches, ants, and spiders.', 1200, 90, 'fixed', False),
    ('Termite Treatment', 'Pest Control', 'Advanced termite control with warranty.', 5000, 180, 'negotiable', False),
    ('Mosquito Fogging', 'Pest Control', 'Professional mosquito control for outdoor areas.', 800, 45, 'fixed', True),
    ('Garden Maintenance', 'Landscaping', 'Regular garden maintenance including mowing and trimming.', 2000, 180, 'fixed', False),
    ('Landscape Design & Setup', 'Landscaping', 'Complete landscape design and installation.', 35000, 960, 'negotiable', False),
    ('Tree Pruning & Removal', 'Landscaping', 'Safe tree pruning and removal service.', 3500, 240, 'negotiable', False),
]

count = 0
for i, (title, cat_name, desc, price, duration, pricing, emergency) in enumerate(services):
    service, created = Service.objects.get_or_create(
        title=title,
        provider=providers[i % len(providers)],
        defaults={
            'category': categories[cat_name],
            'description': desc,
            'price': price,
            'duration_minutes': duration,
            'pricing_type': pricing,
            'is_emergency_available': emergency,
            'is_available': True,
        }
    )
    if created:
        count += 1
        print(f'✓ Created: {title}')

print(f'\n{"="*60}')
print(f'Created {count} new services!')
print(f'Total services: {Service.objects.count()}')
print(f'{"="*60}')
