import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'homeserve.settings')
django.setup()

from services.models import Service

# Approve all services
count = Service.objects.all().update(approval_status='approved')
print(f'Approved {count} services')

# Show status
approved = Service.objects.filter(approval_status='approved').count()
pending = Service.objects.filter(approval_status='pending').count()
total = Service.objects.count()

print(f'\nStatus summary:')
print(f'Total services: {total}')
print(f'Approved: {approved}')
print(f'Pending: {pending}')
