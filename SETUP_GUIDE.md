# HomeServe - Complete Setup & Testing Guide

## 📋 Table of Contents
1. [Prerequisites](#prerequisites)
2. [Installation Steps](#installation-steps)
3. [Creating Test Data](#creating-test-data)
4. [Admin Panel Testing](#admin-panel-testing)
5. [REST API Testing](#rest-api-testing)
6. [Common Issues & Solutions](#common-issues--solutions)

---

## Prerequisites

### Required Software
- Python 3.12+
- pip (Python package manager)
- Virtual environment (recommended)
- Git (for version control)
- Postman or cURL (for API testing)

### System Requirements
- Windows/Linux/macOS
- 500MB free disk space
- 2GB RAM minimum

---

## Installation Steps

### Step 1: Navigate to Project Directory
```powershell
cd c:\entry\frontend\django_folder\homeserve
```

### Step 2: Activate Virtual Environment
```powershell
# From django_folder directory
..\my_virtual\Scripts\Activate.ps1
```

**Alternative (if execution policy error):**
```powershell
# From homeserve directory
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### Step 3: Install Dependencies
```powershell
pip install django djangorestframework django-filter django-cors-headers Pillow
```

**Expected packages:**
- Django 5.2.8
- djangorestframework 3.16.1
- django-filter 25.2
- django-cors-headers 4.9.0
- Pillow 12.0.0

### Step 4: Verify Installation
```powershell
python manage.py check
```

**Expected output:** `System check identified no issues (0 silenced).`

### Step 5: Run Migrations (if not already done)
```powershell
python manage.py makemigrations
python manage.py migrate
```

### Step 6: Create Superuser
```powershell
python manage.py createsuperuser
```

**Sample credentials:**
- Username: `admin`
- Email: `admin@homeserve.com`
- Password: `admin123` (use a strong password in production)

### Step 7: Create Media Directories
```powershell
mkdir media
mkdir media\providers
mkdir media\services
mkdir media\reviews
mkdir media\portfolio
mkdir media\verification_docs
```

### Step 8: Start Development Server
```powershell
python manage.py runserver
```

**Server should start at:** `http://127.0.0.1:8000/`

---

## Creating Test Data

### Method 1: Using Admin Panel (Recommended)

#### 1. Access Admin Panel
- URL: `http://127.0.0.1:8000/admin/`
- Login with superuser credentials

#### 2. Create Service Categories
Navigate to **Service Categories** → **Add Service Category**

**Sample Categories:**
```
Category 1:
- Name: Plumbing
- Description: Professional plumbing services for homes and offices
- Icon: 🔧
- Is Active: ✓

Category 2:
- Name: Electrical Work
- Description: Licensed electricians for all electrical needs
- Icon: ⚡
- Is Active: ✓

Category 3:
- Name: Home Cleaning
- Description: Professional cleaning services for residential spaces
- Icon: 🧹
- Is Active: ✓

Category 4:
- Name: AC Repair
- Description: Air conditioning installation and repair services
- Icon: ❄️
- Is Active: ✓

Category 5:
- Name: Carpentry
- Description: Custom woodwork and furniture repair
- Icon: 🪚
- Is Active: ✓
```

#### 3. Create Users for Service Providers
Navigate to **Users** → **Add User**

**Sample Users:**
```
User 1:
- Username: john_plumber
- Password: test123
- First name: John
- Last name: Smith
- Email: john@plumbing.com

User 2:
- Username: sarah_electric
- Password: test123
- First name: Sarah
- Last name: Johnson
- Email: sarah@electric.com

User 3:
- Username: mike_cleaner
- Password: test123
- First name: Mike
- Last name: Wilson
- Email: mike@cleaning.com
```

#### 4. Create Service Providers
Navigate to **Service Providers** → **Add Service Provider**

**Sample Provider 1:**
```
User: john_plumber
Business Name: Smith Plumbing Services
Contact Number: +1234567890
Email: john@plumbing.com
Address: 123 Main Street
City: New York
State: NY
Pincode: 10001
Experience Years: 5
Bio: Professional plumber with 5 years of experience in residential and commercial plumbing
Verification Status: Verified
Is Available: ✓
Available From: 09:00
Available To: 18:00
```

**Sample Provider 2:**
```
User: sarah_electric
Business Name: Johnson Electricals
Contact Number: +1234567891
Email: sarah@electric.com
Address: 456 Oak Avenue
City: Los Angeles
State: CA
Pincode: 90001
Experience Years: 8
Bio: Licensed electrician specializing in home wiring and repairs
Verification Status: Verified
Is Available: ✓
Available From: 08:00
Available To: 17:00
```

**Sample Provider 3:**
```
User: mike_cleaner
Business Name: Wilson Cleaning Co.
Contact Number: +1234567892
Email: mike@cleaning.com
Address: 789 Pine Road
City: Chicago
State: IL
Pincode: 60601
Experience Years: 3
Bio: Eco-friendly cleaning services for homes and offices
Verification Status: Pending
Is Available: ✓
Available From: 07:00
Available To: 19:00
```

#### 5. Create Services
Navigate to **Services** → **Add Service**

**Sample Service 1:**
```
Provider: Smith Plumbing Services
Category: Plumbing
Title: Leak Repair & Pipe Fixing
Description: Expert repair of leaking pipes, faucets, and drainage systems
Pricing Type: Fixed Price
Price: 75.00
Duration Minutes: 90
Is Active: ✓
Is Emergency Available: ✓
```

**Sample Service 2:**
```
Provider: Smith Plumbing Services
Category: Plumbing
Title: Bathroom Installation
Description: Complete bathroom plumbing installation including fixtures
Pricing Type: Negotiable
Price: 500.00
Duration Minutes: 480
Is Active: ✓
Is Emergency Available: ✗
```

**Sample Service 3:**
```
Provider: Johnson Electricals
Category: Electrical Work
Title: Home Wiring & Rewiring
Description: Complete electrical wiring services for homes
Pricing Type: Hourly Rate
Price: 50.00
Duration Minutes: 60
Is Active: ✓
Is Emergency Available: ✓
```

**Sample Service 4:**
```
Provider: Wilson Cleaning Co.
Category: Home Cleaning
Title: Deep House Cleaning
Description: Comprehensive cleaning service for entire house
Pricing Type: Fixed Price
Price: 150.00
Duration Minutes: 240
Is Active: ✓
Is Emergency Available: ✗
```

#### 6. Create Customer User
```
Username: customer1
Password: test123
First name: Alice
Last name: Brown
Email: alice@customer.com
```

#### 7. Create Bookings
Navigate to **Bookings** → **Add Booking**

**Sample Booking 1:**
```
Customer: customer1
Service: Leak Repair & Pipe Fixing
Provider: Smith Plumbing Services (auto-filled)
Booking Date: [Tomorrow's date]
Booking Time: 10:00
Address: 321 Customer Street
City: New York
Pincode: 10002
Customer Notes: Kitchen sink is leaking badly
Estimated Duration: 90
Status: Pending Confirmation
Total Amount: 75.00
Payment Status: Pending
```

**Sample Booking 2:**
```
Customer: customer1
Service: Deep House Cleaning
Provider: Wilson Cleaning Co. (auto-filled)
Booking Date: [Day after tomorrow]
Booking Time: 09:00
Address: 321 Customer Street
City: New York
Pincode: 10002
Customer Notes: Need deep cleaning before guests arrive
Estimated Duration: 240
Status: Confirmed
Total Amount: 150.00
Payment Status: Paid
```

#### 8. Create Reviews (After Completed Bookings)
First, mark a booking as completed:
1. Go to **Bookings**
2. Select a booking
3. Change Status to "Completed"
4. Save

Then create review:
Navigate to **Reviews** → **Add Review**

**Sample Review:**
```
Booking: [Select completed booking]
Provider: [Auto-filled from booking]
Customer: [Auto-filled from booking]
Rating: 5
Review Text: Excellent service! John arrived on time and fixed the leak quickly. Very professional and cleaned up after the work. Highly recommended!
```

---

## Admin Panel Testing

### Test Scenario 1: Provider Verification Workflow

**Steps:**
1. Login as admin: `http://127.0.0.1:8000/admin/`
2. Go to **Service Providers**
3. Find provider with "Pending" status (orange badge)
4. Select the provider checkbox
5. From Actions dropdown, select "Verify selected providers"
6. Click "Go"
7. Verify status changes to "Verified" (green badge)

**Expected Results:**
- ✓ Status badge changes from orange to green
- ✓ Verified timestamp is set
- ✓ Success message appears

### Test Scenario 2: Booking Management

**Steps:**
1. Go to **Bookings**
2. View booking with "Pending" status (orange badge)
3. Select booking checkbox
4. Choose "Confirm selected bookings" action
5. Click "Go"
6. Open the booking to verify changes

**Expected Results:**
- ✓ Status changes to "Confirmed" (blue badge)
- ✓ Confirmed timestamp is set
- ✓ Success message appears

**Complete Booking:**
1. Select confirmed booking
2. Choose "Mark as completed" action
3. Click "Go"

**Expected Results:**
- ✓ Status changes to "Completed" (green badge)
- ✓ Completed timestamp is set
- ✓ Provider's total bookings count increases

### Test Scenario 3: Search & Filter

**Test Filters:**
1. **Provider Filter:**
   - Filter by City: Select "New York"
   - Verify only NY providers show
   
2. **Service Filter:**
   - Filter by Category: Select "Plumbing"
   - Verify only plumbing services show
   
3. **Booking Filter:**
   - Filter by Status: Select "Confirmed"
   - Filter by Payment Status: Select "Paid"
   - Verify filtered results

**Test Search:**
1. In Services, search "leak"
2. Verify "Leak Repair" service appears
3. Search "cleaning"
4. Verify cleaning services appear

### Test Scenario 4: Review Management

**Steps:**
1. Go to **Reviews**
2. View review list with star ratings
3. Click on a review
4. Add provider response:
   - Provider Response: "Thank you for your kind words! It was a pleasure serving you."
5. Save
6. Verify "Responded" status appears in list

**Expected Results:**
- ✓ Provider response saved
- ✓ Response timestamp set
- ✓ Status shows "✓ Responded" in list

---

## REST API Testing

### Using Browser (Simple GET Requests)

**Test URLs in browser:**
```
http://127.0.0.1:8000/api/categories/
http://127.0.0.1:8000/api/providers/
http://127.0.0.1:8000/api/services/
http://127.0.0.1:8000/api/bookings/
http://127.0.0.1:8000/api/reviews/
```

### Using PowerShell/cURL

#### 1. List All Categories
```powershell
curl http://127.0.0.1:8000/api/categories/
```

**Expected Response:**
```json
{
  "count": 5,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "name": "Plumbing",
      "description": "Professional plumbing services...",
      "icon": "🔧",
      "is_active": true,
      "total_services": 2
    }
  ]
}
```

#### 2. List All Verified Providers
```powershell
curl http://127.0.0.1:8000/api/providers/
```

#### 3. Get Provider Details
```powershell
curl http://127.0.0.1:8000/api/providers/1/
```

#### 4. Get Provider's Services
```powershell
curl http://127.0.0.1:8000/api/providers/1/services/
```

#### 5. Get Provider's Reviews
```powershell
curl http://127.0.0.1:8000/api/providers/1/reviews/
```

#### 6. Search Services
```powershell
# Search by keyword
curl "http://127.0.0.1:8000/api/services/search/?q=leak"

# Search by city
curl "http://127.0.0.1:8000/api/services/search/?city=New York"

# Search by max price
curl "http://127.0.0.1:8000/api/services/search/?max_price=100"

# Combined search
curl "http://127.0.0.1:8000/api/services/search/?q=plumbing&city=New York&max_price=200"
```

#### 7. Filter Services
```powershell
# By category
curl "http://127.0.0.1:8000/api/services/?category=1"

# By pricing type
curl "http://127.0.0.1:8000/api/services/?pricing_type=fixed"

# Emergency services only
curl "http://127.0.0.1:8000/api/services/?is_emergency_available=true"
```

### Using Postman

#### Setup Postman Collection

**Create new collection:** "HomeServe API"

**Add these requests:**

##### 1. Get All Categories
- Method: GET
- URL: `http://127.0.0.1:8000/api/categories/`

##### 2. Create Category (Admin)
- Method: POST
- URL: `http://127.0.0.1:8000/api/categories/`
- Headers: `Content-Type: application/json`
- Body (JSON):
```json
{
  "name": "Painting",
  "description": "Professional painting services",
  "icon": "🎨",
  "is_active": true
}
```

##### 3. Get Provider Services
- Method: GET
- URL: `http://127.0.0.1:8000/api/providers/1/services/`

##### 4. Create Service Request
- Method: POST
- URL: `http://127.0.0.1:8000/api/service-requests/`
- Body (JSON):
```json
{
  "category_id": 1,
  "title": "Urgent Pipe Burst",
  "description": "Main water pipe burst in basement",
  "urgency": "emergency",
  "address": "123 Emergency Street",
  "city": "New York",
  "pincode": "10001",
  "budget_min": 100,
  "budget_max": 300
}
```

##### 5. Confirm Booking (Provider)
- Method: POST
- URL: `http://127.0.0.1:8000/api/bookings/1/confirm/`
- Note: Must be authenticated as provider

##### 6. Complete Booking (Provider)
- Method: POST
- URL: `http://127.0.0.1:8000/api/bookings/1/complete/`

##### 7. Create Review
- Method: POST
- URL: `http://127.0.0.1:8000/api/reviews/`
- Body (JSON):
```json
{
  "booking_id": 1,
  "rating": 5,
  "review_text": "Excellent service!"
}
```

---

## Testing Checklist

### Admin Panel Testing
- [ ] Login as admin
- [ ] Create service categories (minimum 5)
- [ ] Create users for providers (minimum 3)
- [ ] Create service providers with different statuses
- [ ] Verify a pending provider
- [ ] Reject a provider
- [ ] Create services for each provider (minimum 2 each)
- [ ] Create customer user
- [ ] Create bookings with different statuses
- [ ] Confirm a pending booking
- [ ] Complete a confirmed booking
- [ ] Cancel a booking
- [ ] Create reviews for completed bookings
- [ ] Add provider response to reviews
- [ ] Test search functionality
- [ ] Test filter combinations
- [ ] Test sorting (by rating, date, price)

### API Testing
- [ ] GET all categories
- [ ] GET all providers
- [ ] GET provider details
- [ ] GET provider services
- [ ] GET provider reviews
- [ ] GET all services
- [ ] Search services by keyword
- [ ] Filter services by category
- [ ] Filter services by city
- [ ] Filter services by price
- [ ] GET emergency services only
- [ ] GET all service requests
- [ ] Create service request
- [ ] Assign provider to request
- [ ] GET bookings (as customer)
- [ ] Confirm booking (as provider)
- [ ] Complete booking (as provider)
- [ ] Cancel booking
- [ ] GET all reviews
- [ ] Filter reviews by rating
- [ ] GET portfolio items

---

## Common Issues & Solutions

### Issue 1: Module Not Found Error
**Error:** `ModuleNotFoundError: No module named 'rest_framework'`

**Solution:**
```powershell
pip install djangorestframework django-filter django-cors-headers Pillow
```

### Issue 2: Migration Error
**Error:** `django.db.migrations.exceptions.InconsistentMigrationHistory`

**Solution:**
```powershell
python manage.py migrate --run-syncdb
```

### Issue 3: Static Files Not Loading
**Error:** Admin panel looks broken (no CSS)

**Solution:**
```powershell
python manage.py collectstatic
```

### Issue 4: Image Upload Error
**Error:** `SuspiciousFileOperation` when uploading images

**Solution:**
Ensure media directories exist:
```powershell
mkdir media\providers
mkdir media\services
mkdir media\reviews
```

### Issue 5: CORS Error (Frontend Integration)
**Error:** `CORS policy: No 'Access-Control-Allow-Origin' header`

**Solution:**
Check settings.py has:
```python
INSTALLED_APPS = [
    ...
    'corsheaders',
]

MIDDLEWARE = [
    ...
    'corsheaders.middleware.CorsMiddleware',
    ...
]

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
]
```

### Issue 6: Port Already in Use
**Error:** `Error: That port is already in use.`

**Solution:**
```powershell
# Use different port
python manage.py runserver 8080

# Or find and kill process using port 8000
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### Issue 7: Virtual Environment Not Activating
**Error:** `Execution policy error`

**Solution:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

## Quick Start Commands

```powershell
# Navigate to project
cd c:\entry\frontend\django_folder\homeserve

# Activate virtual environment (from django_folder)
..\my_virtual\Scripts\Activate.ps1

# Create superuser (if not done)
python manage.py createsuperuser

# Run server
python manage.py runserver

# Access admin panel
# Open browser: http://127.0.0.1:8000/admin/

# Access API root
# Open browser: http://127.0.0.1:8000/api/
```

---

## Next Steps After Setup

1. ✅ Create comprehensive test data (categories, providers, services)
2. ✅ Test all admin panel features
3. ✅ Test all API endpoints
4. ✅ Take screenshots for documentation
5. ✅ Test user workflows (customer booking, provider confirming)
6. ✅ Test edge cases (cancellations, rejections)
7. ✅ Review rating calculation logic
8. ✅ Test search and filter combinations

---

**Need Help?**
- Check Django documentation: https://docs.djangoproject.com/
- DRF documentation: https://www.django-rest-framework.org/
- Project issues: Review error logs in terminal

**Ready for deployment to:**
- PythonAnywhere
- Heroku
- AWS/Azure
- DigitalOcean
