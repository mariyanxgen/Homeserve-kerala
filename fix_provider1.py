import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'homeserve.settings')
django.setup()

from django.contrib.auth.models import User
from services.models import ServiceProvider
from django.utils import timezone

# Check and fix provider1
try:
    u = User.objects.get(username='provider1')
    print(f"User 'provider1' exists")
    
    try:
        sp = u.provider_profile
        print(f"Provider profile exists: {sp.business_name}")
        print(f"Status: {sp.verification_status}")
    except:
        print("No provider profile - creating one now...")
        
        # Create provider profile
        sp = ServiceProvider.objects.create(
            user=u,
            business_name='Provider1 Home Services',
            contact_number='9876543210',
            email=u.email or 'provider1@homeserve.com',
            address='100 Service Road',
            city='Kochi',
            state='Kerala',
            pincode='682001',
            experience_years=10,
            bio='Experienced home service provider with 10 years of expertise',
            verification_status='verified',
            verified_at=timezone.now(),
            is_available=True,
            average_rating=4.5,
        )
        print(f"Created provider profile: {sp.business_name}")
        print("SUCCESS - provider1 now has a provider dashboard!")
        
except User.DoesNotExist:
    print("User 'provider1' does not exist")
