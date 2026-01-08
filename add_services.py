"""
Script to add diverse services to the HomeServe database
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'homeserve.settings')
django.setup()

from services.models import ServiceCategory, ServiceProvider, Service
from django.contrib.auth.models import User

def create_services():
    """Create diverse services across different categories"""
    
    # Get or create categories
    categories = {
        'Plumbing': ServiceCategory.objects.get_or_create(
            name='Plumbing',
            defaults={'description': 'Professional plumbing services'}
        )[0],
        'Electrical': ServiceCategory.objects.get_or_create(
            name='Electrical',
            defaults={'description': 'Electrical installation and repair'}
        )[0],
        'Cleaning': ServiceCategory.objects.get_or_create(
            name='Cleaning',
            defaults={'description': 'Home and office cleaning services'}
        )[0],
        'Carpentry': ServiceCategory.objects.get_or_create(
            name='Carpentry',
            defaults={'description': 'Wood work and furniture services'}
        )[0],
        'Painting': ServiceCategory.objects.get_or_create(
            name='Painting',
            defaults={'description': 'Interior and exterior painting'}
        )[0],
        'AC Repair': ServiceCategory.objects.get_or_create(
            name='AC Repair',
            defaults={'description': 'Air conditioning repair and maintenance'}
        )[0],
        'Pest Control': ServiceCategory.objects.get_or_create(
            name='Pest Control',
            defaults={'description': 'Professional pest control services'}
        )[0],
        'Landscaping': ServiceCategory.objects.get_or_create(
            name='Landscaping',
            defaults={'description': 'Garden and lawn maintenance'}
        )[0],
    }
    
    # Get or create sample providers
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
    
    # Define services to create
    services_data = [
        # Plumbing Services
        {
            'title': 'Emergency Pipe Leak Repair',
            'category': categories['Plumbing'],
            'description': 'Quick response for urgent pipe leak repairs. Our experienced plumbers will fix all types of leaks including kitchen, bathroom, and underground pipes. Available 24/7 for emergencies.',
            'price': 800,
            'duration_minutes': 60,
            'pricing_type': 'fixed',
            'is_emergency_available': True,
            'district': 'Thiruvananthapuram'
        },
        {
            'title': 'Bathroom Fittings Installation',
            'category': categories['Plumbing'],
            'description': 'Complete bathroom fitting installation including taps, showers, toilets, and drainage systems. Professional installation with warranty on workmanship.',
            'price': 2500,
            'duration_minutes': 180,
            'pricing_type': 'fixed',
            'is_emergency_available': False,
            'district': 'Kochi'
        },
        {
            'title': 'Water Tank Cleaning',
            'category': categories['Plumbing'],
            'description': 'Thorough water tank cleaning and sanitization service. Includes removal of sediments, algae cleaning, and disinfection to ensure safe drinking water.',
            'price': 1500,
            'duration_minutes': 120,
            'pricing_type': 'fixed',
            'is_emergency_available': False,
            'district': 'Kozhikode'
        },
        
        # Electrical Services
        {
            'title': 'Complete Home Wiring',
            'category': categories['Electrical'],
            'description': 'Full house electrical wiring service with modern standards. Includes conduit installation, wiring, switchboard setup, and safety certification.',
            'price': 15000,
            'duration_minutes': 480,
            'pricing_type': 'negotiable',
            'is_emergency_available': False,
            'district': 'Thrissur'
        },
        {
            'title': 'Fan & Light Installation',
            'category': categories['Electrical'],
            'description': 'Professional installation of ceiling fans, lights, and other electrical fixtures. Includes proper mounting and electrical connections.',
            'price': 500,
            'duration_minutes': 45,
            'pricing_type': 'fixed',
            'is_emergency_available': True,
            'district': 'Kollam'
        },
        {
            'title': 'Electrical Safety Inspection',
            'category': categories['Electrical'],
            'description': 'Comprehensive electrical safety check for your home. Identify potential hazards, faulty wiring, and recommend improvements.',
            'price': 1200,
            'duration_minutes': 90,
            'pricing_type': 'fixed',
            'is_emergency_available': False,
            'district': 'Thiruvananthapuram'
        },
        
        # Cleaning Services
        {
            'title': 'Deep House Cleaning',
            'category': categories['Cleaning'],
            'description': 'Comprehensive deep cleaning service for your entire home. Includes kitchen, bathrooms, bedrooms, living areas, and balconies. Professional cleaning products included.',
            'price': 3000,
            'duration_minutes': 240,
            'pricing_type': 'fixed',
            'is_emergency_available': False,
            'district': 'Kochi'
        },
        {
            'title': 'Sofa & Carpet Cleaning',
            'category': categories['Cleaning'],
            'description': 'Professional upholstery and carpet cleaning using advanced steam cleaning technology. Removes stains, odors, and allergens.',
            'price': 1800,
            'duration_minutes': 120,
            'pricing_type': 'fixed',
            'is_emergency_available': False,
            'district': 'Kozhikode'
        },
        {
            'title': 'Kitchen Deep Cleaning',
            'category': categories['Cleaning'],
            'description': 'Specialized kitchen cleaning including chimney, stove, tiles, cabinets, and exhaust fans. Remove grease and grime buildup.',
            'price': 1500,
            'duration_minutes': 150,
            'pricing_type': 'fixed',
            'is_emergency_available': False,
            'district': 'Thrissur'
        },
        
        # Carpentry Services
        {
            'title': 'Custom Furniture Making',
            'category': categories['Carpentry'],
            'description': 'Bespoke furniture creation including wardrobes, beds, tables, and storage units. High-quality wood and finish with design consultation.',
            'price': 25000,
            'duration_minutes': 720,
            'pricing_type': 'negotiable',
            'is_emergency_available': False,
            'district': 'Kollam'
        },
        {
            'title': 'Door & Window Repair',
            'category': categories['Carpentry'],
            'description': 'Repair and maintenance of wooden doors and windows. Includes fixing hinges, locks, alignment issues, and wood restoration.',
            'price': 800,
            'duration_minutes': 90,
            'pricing_type': 'fixed',
            'is_emergency_available': True,
            'district': 'Thiruvananthapuram'
        },
        {
            'title': 'Modular Kitchen Installation',
            'category': categories['Carpentry'],
            'description': 'Complete modular kitchen installation with cabinets, drawers, and counter tops. Professional installation with warranty.',
            'price': 45000,
            'duration_minutes': 960,
            'pricing_type': 'negotiable',
            'is_emergency_available': False,
            'district': 'Kochi'
        },
        
        # Painting Services
        {
            'title': 'Interior Wall Painting',
            'category': categories['Painting'],
            'description': 'Complete interior painting service with premium quality paints. Includes surface preparation, putty work, primer, and two coats of paint.',
            'price': 18,
            'duration_minutes': 480,
            'pricing_type': 'hourly',
            'is_emergency_available': False,
            'district': 'Kozhikode'
        },
        {
            'title': 'Exterior Wall Painting',
            'category': categories['Painting'],
            'description': 'Weather-resistant exterior painting service. Includes wall cleaning, crack filling, waterproofing, and durable paint application.',
            'price': 22,
            'duration_minutes': 600,
            'pricing_type': 'hourly',
            'is_emergency_available': False,
            'district': 'Thrissur'
        },
        {
            'title': 'Texture & Design Painting',
            'category': categories['Painting'],
            'description': 'Decorative texture painting and design work for feature walls. Multiple design options and color combinations available.',
            'price': 3500,
            'duration_minutes': 300,
            'pricing_type': 'negotiable',
            'is_emergency_available': False,
            'district': 'Kollam'
        },
        
        # AC Repair Services
        {
            'title': 'AC Installation & Setup',
            'category': categories['AC Repair'],
            'description': 'Professional air conditioner installation service for split and window AC units. Includes mounting, piping, and gas charging.',
            'price': 2500,
            'duration_minutes': 120,
            'pricing_type': 'fixed',
            'is_emergency_available': False,
            'district': 'Thiruvananthapuram'
        },
        {
            'title': 'AC Service & Maintenance',
            'category': categories['AC Repair'],
            'description': 'Regular AC servicing including filter cleaning, coil cleaning, gas pressure check, and general maintenance for optimal performance.',
            'price': 600,
            'duration_minutes': 60,
            'pricing_type': 'fixed',
            'is_emergency_available': True,
            'district': 'Kochi'
        },
        {
            'title': 'AC Gas Refilling',
            'category': categories['AC Repair'],
            'description': 'AC gas refilling and leak detection service. Ensures proper cooling efficiency and identifies any refrigerant leaks.',
            'price': 1800,
            'duration_minutes': 90,
            'pricing_type': 'fixed',
            'is_emergency_available': True,
            'district': 'Kozhikode'
        },
        
        # Pest Control Services
        {
            'title': 'General Pest Control',
            'category': categories['Pest Control'],
            'description': 'Comprehensive pest control treatment for cockroaches, ants, spiders, and other common household pests. Safe for children and pets.',
            'price': 1200,
            'duration_minutes': 90,
            'pricing_type': 'fixed',
            'is_emergency_available': False,
            'district': 'Thrissur'
        },
        {
            'title': 'Termite Treatment',
            'category': categories['Pest Control'],
            'description': 'Advanced termite control treatment with pre and post-construction options. Includes inspection, treatment, and warranty.',
            'price': 5000,
            'duration_minutes': 180,
            'pricing_type': 'negotiable',
            'is_emergency_available': False,
            'district': 'Kollam'
        },
        {
            'title': 'Mosquito Fogging',
            'category': categories['Pest Control'],
            'description': 'Professional mosquito control using fogging technique. Effective for outdoor areas, gardens, and premises.',
            'price': 800,
            'duration_minutes': 45,
            'pricing_type': 'fixed',
            'is_emergency_available': True,
            'district': 'Thiruvananthapuram'
        },
        
        # Landscaping Services
        {
            'title': 'Garden Maintenance',
            'category': categories['Landscaping'],
            'description': 'Regular garden maintenance including lawn mowing, hedge trimming, weeding, and plant care. Monthly package available.',
            'price': 2000,
            'duration_minutes': 180,
            'pricing_type': 'fixed',
            'is_emergency_available': False,
            'district': 'Kochi'
        },
        {
            'title': 'Landscape Design & Setup',
            'category': categories['Landscaping'],
            'description': 'Complete landscape design and installation service. Includes planning, plant selection, lawn setup, and decorative elements.',
            'price': 35000,
            'duration_minutes': 960,
            'pricing_type': 'negotiable',
            'is_emergency_available': False,
            'district': 'Kozhikode'
        },
        {
            'title': 'Tree Pruning & Removal',
            'category': categories['Landscaping'],
            'description': 'Professional tree pruning, trimming, and removal service. Safe removal of dead or dangerous trees with proper equipment.',
            'price': 3500,
            'duration_minutes': 240,
            'pricing_type': 'negotiable',
            'is_emergency_available': False,
            'district': 'Thrissur'
        },
    ]
    
    # Create services
    created_count = 0
    for i, service_data in enumerate(services_data):
        provider = providers[i % len(providers)]
        
        service, created = Service.objects.get_or_create(
            title=service_data['title'],
            provider=provider,
            defaults={
                'category': service_data['category'],
                'description': service_data['description'],
                'price': service_data['price'],
                'duration_minutes': service_data['duration_minutes'],
                'pricing_type': service_data['pricing_type'],
                'is_emergency_available': service_data['is_emergency_available'],
                'is_available': True,
            }
        )
        
        if created:
            created_count += 1
            print(f"✓ Created: {service_data['title']} - {service_data['category'].name}")
        else:
            print(f"  Already exists: {service_data['title']}")
    
    print(f"\n{'='*60}")
    print(f"Summary: {created_count} new services created!")
    print(f"Total services in database: {Service.objects.count()}")
    print(f"{'='*60}")

if __name__ == '__main__':
    create_services()
