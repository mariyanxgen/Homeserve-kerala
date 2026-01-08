from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from services.models import ServiceCategory, ServiceProvider, Service


class Command(BaseCommand):
    help = 'Add sample services to the database'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Adding services to database...'))
        
        # Create categories
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
            cat, created = ServiceCategory.objects.get_or_create(
                name=name, 
                defaults={'description': desc, 'is_active': True}
            )
            categories[name] = cat
            if created:
                self.stdout.write(f'✓ Created category: {name}')
        
        # Create providers
        providers = []
        districts = ['Thiruvananthapuram', 'Kochi', 'Kozhikode', 'Thrissur', 'Kollam']
        
        for i in range(5):
            user, _ = User.objects.get_or_create(
                username=f'provider{i+1}',
                defaults={
                    'email': f'provider{i+1}@homeserve.com',
                    'first_name': f'Provider',
                    'last_name': f'{i+1}'
                }
            )
            
            provider, created = ServiceProvider.objects.get_or_create(
                user=user,
                defaults={
                    'business_name': f'{districts[i]} Pro Services',
                    'contact_number': f'98765432{i}0',
                    'email': f'contact@provider{i+1}.com',
                    'address': f'{i+1}23 Main Road, {districts[i]}',
                    'city': districts[i],
                    'state': 'Kerala',
                    'pincode': f'68000{i}',
                    'verification_status': 'verified',
                    'experience_years': 5 + i,
                    'is_available': True
                }
            )
            providers.append(provider)
            if created:
                self.stdout.write(f'✓ Created provider: {provider.business_name}')
        
        # Create services
        services_data = [
            # Plumbing
            ('Emergency Pipe Leak Repair', 'Plumbing', 'Quick response for urgent pipe leak repairs. Our experienced plumbers will fix all types of leaks. Available 24/7.', 800, 60, 'fixed', True),
            ('Bathroom Fittings Installation', 'Plumbing', 'Complete bathroom fitting installation including taps, showers, and toilets with warranty.', 2500, 180, 'fixed', False),
            ('Water Tank Cleaning', 'Plumbing', 'Thorough water tank cleaning and sanitization service for safe drinking water.', 1500, 120, 'fixed', False),
            
            # Electrical
            ('Complete Home Wiring', 'Electrical', 'Full house electrical wiring with modern safety standards and certification.', 15000, 480, 'negotiable', False),
            ('Fan & Light Installation', 'Electrical', 'Professional installation of ceiling fans, lights, and fixtures.', 500, 45, 'fixed', True),
            ('Electrical Safety Inspection', 'Electrical', 'Comprehensive electrical safety check to identify potential hazards.', 1200, 90, 'fixed', False),
            
            # Cleaning
            ('Deep House Cleaning', 'Cleaning', 'Comprehensive deep cleaning for entire home including all rooms and surfaces.', 3000, 240, 'fixed', False),
            ('Sofa & Carpet Cleaning', 'Cleaning', 'Professional upholstery cleaning using advanced steam cleaning technology.', 1800, 120, 'fixed', False),
            ('Kitchen Deep Cleaning', 'Cleaning', 'Specialized kitchen cleaning including chimney, tiles, and exhaust fans.', 1500, 150, 'fixed', False),
            
            # Carpentry
            ('Custom Furniture Making', 'Carpentry', 'Bespoke furniture creation with high-quality wood and professional design consultation.', 25000, 720, 'negotiable', False),
            ('Door & Window Repair', 'Carpentry', 'Repair and maintenance of wooden doors and windows including hinges and locks.', 800, 90, 'fixed', True),
            ('Modular Kitchen Installation', 'Carpentry', 'Complete modular kitchen installation with cabinets and warranty.', 45000, 960, 'negotiable', False),
            
            # Painting
            ('Interior Wall Painting', 'Painting', 'Complete interior painting with premium quality paints and surface preparation.', 18, 480, 'hourly', False),
            ('Exterior Wall Painting', 'Painting', 'Weather-resistant exterior painting with waterproofing and durable paint.', 22, 600, 'hourly', False),
            ('Texture & Design Painting', 'Painting', 'Decorative texture painting for feature walls with multiple design options.', 3500, 300, 'negotiable', False),
            
            # AC Repair
            ('AC Installation & Setup', 'AC Repair', 'Professional air conditioner installation for split and window AC units.', 2500, 120, 'fixed', False),
            ('AC Service & Maintenance', 'AC Repair', 'Regular AC servicing including filter and coil cleaning for optimal performance.', 600, 60, 'fixed', True),
            ('AC Gas Refilling', 'AC Repair', 'AC gas refilling and leak detection service for proper cooling efficiency.', 1800, 90, 'fixed', True),
            
            # Pest Control
            ('General Pest Control', 'Pest Control', 'Comprehensive treatment for cockroaches, ants, and spiders. Safe for pets.', 1200, 90, 'fixed', False),
            ('Termite Treatment', 'Pest Control', 'Advanced termite control treatment with inspection and warranty.', 5000, 180, 'negotiable', False),
            ('Mosquito Fogging', 'Pest Control', 'Professional mosquito control using fogging for outdoor areas and gardens.', 800, 45, 'fixed', True),
            
            # Landscaping
            ('Garden Maintenance', 'Landscaping', 'Regular garden maintenance including lawn mowing, trimming, and plant care.', 2000, 180, 'fixed', False),
            ('Landscape Design & Setup', 'Landscaping', 'Complete landscape design and installation with planning and plant selection.', 35000, 960, 'negotiable', False),
            ('Tree Pruning & Removal', 'Landscaping', 'Professional tree pruning and safe removal with proper equipment.', 3500, 240, 'negotiable', False),
        ]
        
        count = 0
        for i, (title, cat_name, desc, price, duration, pricing, emergency) in enumerate(services_data):
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
                    'is_active': True,
                }
            )
            if created:
                count += 1
                self.stdout.write(self.style.SUCCESS(f'✓ Created: {title}'))
        
        self.stdout.write(self.style.SUCCESS(f'\n{"="*60}'))
        self.stdout.write(self.style.SUCCESS(f'Successfully added {count} new services!'))
        self.stdout.write(self.style.SUCCESS(f'Total services in database: {Service.objects.count()}'))
        self.stdout.write(self.style.SUCCESS(f'{"="*60}'))
