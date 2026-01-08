#!/usr/bin/env python
import os, sys, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'homeserve.settings')
django.setup()

from services.models import Service, ServiceCategory

total = Service.objects.filter(is_active=True).count()
print(f"Total active services: {total}\n")

print("All categories:")
for cat in ServiceCategory.objects.all():
    count = Service.objects.filter(category=cat, is_active=True).count()
    print(f"  ID {cat.id}: {cat.name} - {count} services")

print("\nSample services:")
for s in Service.objects.filter(is_active=True)[:3]:
    print(f"  {s.id}: {s.title} (Cat: {s.category.name}, City: {s.provider.city})")

# Check the specific issue
ac_repair = ServiceCategory.objects.filter(name__icontains='AC').first()
if ac_repair:
    ac_services = Service.objects.filter(category=ac_repair, is_active=True)
    print(f"\nAC Repair (ID {ac_repair.id}) services: {ac_services.count()}")
    
    thiru_services = Service.objects.filter(provider__city__icontains='Thiruvananthapuram', is_active=True)
    print(f"Services in Thiruvananthapuram: {thiru_services.count()}")
    
    both = Service.objects.filter(category=ac_repair, provider__city__icontains='Thiruvananthapuram', is_active=True)
    print(f"AC Repair + Thiruvananthapuram: {both.count()}")
    
    if both.count() == 0:
        print("\n  AC services:")
        for s in ac_services[:3]:
            print(f"    {s.title} - City: {s.provider.city}")
