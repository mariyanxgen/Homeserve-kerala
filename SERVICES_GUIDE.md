# Adding Services to HomeServe

## Server is Running
Your Django server is now running at: http://127.0.0.1:8000/

## Quick Service Addition Guide

### Method 1: Django Admin Panel (Recommended)
1. Open your browser and go to: http://127.0.0.1:8000/admin/
2. Login with your superuser credentials
3. Click on "Services" under the SERVICES section
4. Click "Add Service +" button
5. Fill in the service details
6. Click "Save"

### Method 2: Bulk Import via Management Command

I've created a script to add 24 diverse services across 8 categories. To run it:

```powershell
cd c:\entry\frontend\django_folder\homeserve
C:\Users\USER\AppData\Local\Programs\Python\Python312\python.exe manage.py shell < load_services.py
```

## Services Being Added

### Plumbing (3 services)
- **Emergency Pipe Leak Repair** - ₹800 (60 min) - Emergency Available
- **Bathroom Fittings Installation** - ₹2,500 (180 min)
- **Water Tank Cleaning** - ₹1,500 (120 min)

### Electrical (3 services)
- **Complete Home Wiring** - ₹15,000 (480 min) - Negotiable
- **Fan & Light Installation** - ₹500 (45 min) - Emergency Available
- **Electrical Safety Inspection** - ₹1,200 (90 min)

### Cleaning (3 services)
- **Deep House Cleaning** - ₹3,000 (240 min)
- **Sofa & Carpet Cleaning** - ₹1,800 (120 min)
- **Kitchen Deep Cleaning** - ₹1,500 (150 min)

### Carpentry (3 services)
- **Custom Furniture Making** - ₹25,000 (720 min) - Negotiable
- **Door & Window Repair** - ₹800 (90 min) - Emergency Available
- **Modular Kitchen Installation** - ₹45,000 (960 min) - Negotiable

### Painting (3 services)
- **Interior Wall Painting** - ₹18/hour (480 min)
- **Exterior Wall Painting** - ₹22/hour (600 min)
- **Texture & Design Painting** - ₹3,500 (300 min) - Negotiable

### AC Repair (3 services)
- **AC Installation & Setup** - ₹2,500 (120 min)
- **AC Service & Maintenance** - ₹600 (60 min) - Emergency Available
- **AC Gas Refilling** - ₹1,800 (90 min) - Emergency Available

### Pest Control (3 services)
- **General Pest Control** - ₹1,200 (90 min)
- **Termite Treatment** - ₹5,000 (180 min) - Negotiable
- **Mosquito Fogging** - ₹800 (45 min) - Emergency Available

### Landscaping (3 services)
- **Garden Maintenance** - ₹2,000 (180 min)
- **Landscape Design & Setup** - ₹35,000 (960 min) - Negotiable
- **Tree Pruning & Removal** - ₹3,500 (240 min) - Negotiable

## Frontend will display these services with:
- Service cards with icons
- Category filters
- Price range filters
- District filters
- Emergency service badges
- Click-to-view details modal
- Book Now functionality

## After Adding Services
1. Visit http://127.0.0.1:8000/ to see the homepage
2. Visit your frontend at frontend/index.html
3. Visit frontend/services.html to browse all services
4. Test the filter functionality
5. Click on service cards to see detail modals
