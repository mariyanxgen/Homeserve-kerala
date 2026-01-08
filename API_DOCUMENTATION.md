# HomeServe REST API Documentation

## 📖 API Overview

Base URL: `http://127.0.0.1:8000/api/`

**Authentication:** Session Authentication (Django built-in)

**Response Format:** JSON

**Pagination:** Enabled (20 items per page by default)

---

## 📚 Table of Contents

1. [Service Categories API](#service-categories-api)
2. [Service Providers API](#service-providers-api)
3. [Services API](#services-api)
4. [Bookings API](#bookings-api)
5. [Reviews API](#reviews-api)
6. [Provider Portfolio API](#provider-portfolio-api)
7. [Service Requests API](#service-requests-api)
8. [Filtering & Search](#filtering--search)
9. [Error Responses](#error-responses)

---

## Service Categories API

### List All Categories
```http
GET /api/categories/
```

**Response:**
```json
{
  "count": 5,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "name": "Plumbing",
      "description": "Professional plumbing services for homes and offices",
      "icon": "🔧",
      "is_active": true,
      "total_services": 4,
      "created_at": "2024-12-15T10:30:00Z"
    }
  ]
}
```

### Create Category
```http
POST /api/categories/
Content-Type: application/json
```

**Request Body:**
```json
{
  "name": "Gardening",
  "description": "Professional gardening and landscaping services",
  "icon": "🌱",
  "is_active": true
}
```

**Response:** `201 Created`
```json
{
  "id": 6,
  "name": "Gardening",
  "description": "Professional gardening and landscaping services",
  "icon": "🌱",
  "is_active": true,
  "total_services": 0,
  "created_at": "2024-12-15T11:00:00Z"
}
```

### Get Category Details
```http
GET /api/categories/{id}/
```

### Update Category
```http
PUT /api/categories/{id}/
PATCH /api/categories/{id}/
```

### Delete Category
```http
DELETE /api/categories/{id}/
```

**Response:** `204 No Content`

---

## Service Providers API

### List All Providers
```http
GET /api/providers/
```

**Query Parameters:**
- `city` - Filter by city
- `state` - Filter by state
- `verification_status` - Filter by status (verified, pending, rejected)
- `is_available` - Filter by availability (true/false)
- `ordering` - Sort by field (average_rating, total_bookings, created_at)
- `search` - Search in business_name, city, bio

**Example:**
```http
GET /api/providers/?city=New York&is_available=true&ordering=-average_rating
```

**Response:**
```json
{
  "count": 3,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "user": {
        "id": 2,
        "username": "john_plumber",
        "email": "john@plumbing.com",
        "first_name": "John",
        "last_name": "Smith"
      },
      "business_name": "Smith Plumbing Services",
      "city": "New York",
      "state": "NY",
      "verification_status": "verified",
      "verification_status_display": "Verified",
      "average_rating": "4.85",
      "total_reviews": 23,
      "total_bookings": 47,
      "is_available": true,
      "profile_image": "/media/providers/john_profile.jpg"
    }
  ]
}
```

### Register as Provider
```http
POST /api/providers/
Content-Type: application/json
```

**Request Body:**
```json
{
  "business_name": "Elite Cleaning Services",
  "contact_number": "+1234567893",
  "email": "info@elitecleaning.com",
  "address": "100 Service Avenue",
  "city": "Boston",
  "state": "MA",
  "pincode": "02101",
  "experience_years": 4,
  "bio": "Professional cleaning services with eco-friendly products",
  "available_from": "08:00",
  "available_to": "18:00"
}
```

**Response:** `201 Created`

### Get Provider Details
```http
GET /api/providers/{id}/
```

**Response:**
```json
{
  "id": 1,
  "user": {
    "id": 2,
    "username": "john_plumber",
    "email": "john@plumbing.com",
    "first_name": "John",
    "last_name": "Smith"
  },
  "business_name": "Smith Plumbing Services",
  "contact_number": "+1234567890",
  "alternate_contact": "",
  "email": "john@plumbing.com",
  "address": "123 Main Street",
  "city": "New York",
  "state": "NY",
  "pincode": "10001",
  "experience_years": 5,
  "bio": "Professional plumber with 5 years of experience",
  "profile_image": "/media/providers/john_profile.jpg",
  "verification_status": "verified",
  "verification_status_display": "Verified",
  "verified_at": "2024-12-01T09:00:00Z",
  "average_rating": "4.85",
  "total_reviews": 23,
  "total_bookings": 47,
  "is_available": true,
  "available_from": "09:00:00",
  "available_to": "18:00:00",
  "services_count": 4,
  "created_at": "2024-11-15T08:30:00Z",
  "updated_at": "2024-12-15T10:00:00Z"
}
```

### Get Provider's Services
```http
GET /api/providers/{id}/services/
```

**Response:**
```json
[
  {
    "id": 1,
    "provider": {...},
    "category": {...},
    "title": "Leak Repair & Pipe Fixing",
    "pricing_type": "fixed",
    "pricing_type_display": "Fixed Price",
    "price": "75.00",
    "duration_minutes": 90,
    "service_image": "/media/services/leak_repair.jpg",
    "is_active": true,
    "is_emergency_available": true,
    "created_at": "2024-12-10T12:00:00Z"
  }
]
```

### Get Provider's Reviews
```http
GET /api/providers/{id}/reviews/
```

### Get Provider's Portfolio
```http
GET /api/providers/{id}/portfolio/
```

### Update Provider Profile
```http
PUT /api/providers/{id}/
PATCH /api/providers/{id}/
```

---

## Services API

### List All Services
```http
GET /api/services/
```

**Query Parameters:**
- `category` - Filter by category ID
- `provider` - Filter by provider ID
- `pricing_type` - Filter by type (fixed, hourly, negotiable)
- `is_emergency_available` - Emergency services only (true/false)
- `ordering` - Sort by (price, created_at, duration_minutes)
- `search` - Search in title, description, provider name

**Example:**
```http
GET /api/services/?category=1&is_emergency_available=true&ordering=price
```

**Response:**
```json
{
  "count": 8,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "provider": {
        "id": 1,
        "business_name": "Smith Plumbing Services",
        "city": "New York",
        "average_rating": "4.85"
      },
      "category": {
        "id": 1,
        "name": "Plumbing",
        "icon": "🔧"
      },
      "title": "Leak Repair & Pipe Fixing",
      "pricing_type": "fixed",
      "pricing_type_display": "Fixed Price",
      "price": "75.00",
      "duration_minutes": 90,
      "service_image": "/media/services/leak_repair.jpg",
      "is_active": true,
      "is_emergency_available": true,
      "created_at": "2024-12-10T12:00:00Z"
    }
  ]
}
```

### Advanced Service Search
```http
GET /api/services/search/
```

**Query Parameters:**
- `q` - Search keyword
- `city` - Filter by provider city
- `max_price` - Maximum price
- `category` - Category ID

**Examples:**
```http
# Search by keyword
GET /api/services/search/?q=leak

# Search by location
GET /api/services/search/?city=New York

# Search by price range
GET /api/services/search/?max_price=100

# Combined search
GET /api/services/search/?q=plumbing&city=New York&max_price=200&category=1
```

**Response:** Same as List Services

### Create Service
```http
POST /api/services/
Content-Type: application/json
```

**Request Body:**
```json
{
  "provider_id": 1,
  "category_id": 1,
  "title": "Emergency Drain Cleaning",
  "description": "24/7 emergency drain cleaning and unclogging services",
  "pricing_type": "fixed",
  "price": "85.00",
  "duration_minutes": 60,
  "is_active": true,
  "is_emergency_available": true
}
```

**Response:** `201 Created`

### Get Service Details
```http
GET /api/services/{id}/
```

### Update Service
```http
PUT /api/services/{id}/
PATCH /api/services/{id}/
```

### Delete Service
```http
DELETE /api/services/{id}/
```

---

## Bookings API

### List User's Bookings
```http
GET /api/bookings/
```

**Note:** Returns bookings where user is either customer or provider

**Query Parameters:**
- `status` - Filter by status (pending, confirmed, in_progress, completed, cancelled, rejected)
- `payment_status` - Filter by payment (pending, paid, refunded)
- `booking_date` - Filter by date (YYYY-MM-DD)
- `ordering` - Sort by (booking_date, created_at)

**Response:**
```json
{
  "count": 5,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "customer": {
        "id": 3,
        "username": "customer1",
        "first_name": "Alice",
        "last_name": "Brown"
      },
      "service": {
        "id": 1,
        "title": "Leak Repair & Pipe Fixing",
        "price": "75.00"
      },
      "provider": {
        "id": 1,
        "business_name": "Smith Plumbing Services",
        "average_rating": "4.85"
      },
      "booking_date": "2024-12-20",
      "booking_time": "10:00:00",
      "city": "New York",
      "status": "confirmed",
      "status_display": "Confirmed",
      "payment_status": "paid",
      "payment_status_display": "Paid",
      "total_amount": "75.00",
      "created_at": "2024-12-15T09:00:00Z"
    }
  ]
}
```

### Create Booking
```http
POST /api/bookings/
Content-Type: application/json
```

**Request Body:**
```json
{
  "service_id": 1,
  "booking_date": "2024-12-20",
  "booking_time": "10:00",
  "address": "321 Customer Street, Apt 5B",
  "city": "New York",
  "pincode": "10002",
  "customer_notes": "Kitchen sink is leaking badly. Please bring necessary tools.",
  "estimated_duration": 90,
  "total_amount": "75.00"
}
```

**Response:** `201 Created`

**Note:** Customer and provider are automatically set from authenticated user and service.

### Get Booking Details
```http
GET /api/bookings/{id}/
```

**Response:**
```json
{
  "id": 1,
  "customer": {...},
  "service": {...},
  "provider": {...},
  "booking_date": "2024-12-20",
  "booking_time": "10:00:00",
  "address": "321 Customer Street, Apt 5B",
  "city": "New York",
  "pincode": "10002",
  "customer_notes": "Kitchen sink is leaking badly",
  "estimated_duration": 90,
  "status": "confirmed",
  "status_display": "Confirmed",
  "total_amount": "75.00",
  "payment_status": "paid",
  "payment_status_display": "Paid",
  "payment_method": "Cash",
  "created_at": "2024-12-15T09:00:00Z",
  "updated_at": "2024-12-15T10:00:00Z",
  "confirmed_at": "2024-12-15T10:00:00Z",
  "completed_at": null
}
```

### Confirm Booking (Provider Only)
```http
POST /api/bookings/{id}/confirm/
```

**Response:**
```json
{
  "id": 1,
  "status": "confirmed",
  "confirmed_at": "2024-12-15T10:30:00Z",
  ...
}
```

### Complete Booking (Provider Only)
```http
POST /api/bookings/{id}/complete/
```

**Response:**
```json
{
  "id": 1,
  "status": "completed",
  "completed_at": "2024-12-20T12:30:00Z",
  ...
}
```

### Cancel Booking
```http
POST /api/bookings/{id}/cancel/
```

**Note:** Both customer and provider can cancel

**Response:**
```json
{
  "id": 1,
  "status": "cancelled",
  ...
}
```

---

## Reviews API

### List All Reviews
```http
GET /api/reviews/
```

**Query Parameters:**
- `provider` - Filter by provider ID
- `rating` - Filter by rating (1-5)
- `ordering` - Sort by (rating, created_at)

**Response:**
```json
{
  "count": 15,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "customer": {
        "id": 3,
        "username": "customer1",
        "first_name": "Alice"
      },
      "provider": {
        "id": 1,
        "business_name": "Smith Plumbing Services"
      },
      "rating": 5,
      "review_text": "Excellent service! Very professional.",
      "image1": "/media/reviews/before1.jpg",
      "image2": "/media/reviews/after1.jpg",
      "image3": null,
      "provider_response": "Thank you for your kind words!",
      "created_at": "2024-12-15T14:00:00Z"
    }
  ]
}
```

### Create Review
```http
POST /api/reviews/
Content-Type: multipart/form-data
```

**Request Body:**
```json
{
  "booking_id": 1,
  "rating": 5,
  "review_text": "Excellent service! John was professional and fixed the leak quickly.",
  "image1": [file upload],
  "image2": [file upload]
}
```

**Response:** `201 Created`

**Note:** Customer and provider are auto-filled from booking

### Get Review Details
```http
GET /api/reviews/{id}/
```

### Update Review
```http
PUT /api/reviews/{id}/
PATCH /api/reviews/{id}/
```

---

## Provider Portfolio API

### List Portfolio Items
```http
GET /api/portfolio/
```

**Query Parameters:**
- `provider` - Filter by provider ID
- `service_category` - Filter by category ID

**Response:**
```json
{
  "count": 8,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "provider": {
        "id": 1,
        "business_name": "Smith Plumbing Services"
      },
      "title": "Bathroom Renovation - Luxury Suite",
      "description": "Complete bathroom renovation with modern fixtures",
      "image": "/media/portfolio/bathroom_renovation.jpg",
      "service_category": {
        "id": 1,
        "name": "Plumbing"
      },
      "created_at": "2024-12-01T10:00:00Z"
    }
  ]
}
```

### Add Portfolio Item
```http
POST /api/portfolio/
Content-Type: multipart/form-data
```

**Request Body:**
```json
{
  "provider_id": 1,
  "title": "Kitchen Sink Installation",
  "description": "Modern double-basin sink installation",
  "image": [file upload],
  "category_id": 1
}
```

### Get Portfolio Item
```http
GET /api/portfolio/{id}/
```

### Update Portfolio Item
```http
PUT /api/portfolio/{id}/
PATCH /api/portfolio/{id}/
```

### Delete Portfolio Item
```http
DELETE /api/portfolio/{id}/
```

---

## Service Requests API

### List Service Requests
```http
GET /api/service-requests/
```

**Query Parameters:**
- `status` - Filter by status (open, assigned, closed)
- `urgency` - Filter by urgency (low, medium, high, emergency)
- `category` - Filter by category ID
- `city` - Filter by city
- `ordering` - Sort by (urgency, created_at)

**Response:**
```json
{
  "count": 3,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "customer": {
        "id": 3,
        "username": "customer1"
      },
      "category": {
        "id": 1,
        "name": "Plumbing"
      },
      "title": "Urgent Pipe Burst",
      "urgency": "emergency",
      "urgency_display": "Emergency",
      "city": "New York",
      "status": "open",
      "status_display": "Open",
      "assigned_provider": null,
      "created_at": "2024-12-15T16:00:00Z"
    }
  ]
}
```

### Create Service Request
```http
POST /api/service-requests/
Content-Type: application/json
```

**Request Body:**
```json
{
  "category_id": 1,
  "title": "Urgent Pipe Burst in Basement",
  "description": "Main water pipe burst causing flooding. Need immediate help!",
  "urgency": "emergency",
  "address": "123 Emergency Street",
  "city": "New York",
  "pincode": "10001",
  "budget_min": "100.00",
  "budget_max": "300.00"
}
```

**Response:** `201 Created`

### Get Service Request Details
```http
GET /api/service-requests/{id}/
```

### Assign Provider to Request
```http
POST /api/service-requests/{id}/assign/
Content-Type: application/json
```

**Request Body:**
```json
{
  "provider_id": 1
}
```

**Response:**
```json
{
  "id": 1,
  "status": "assigned",
  "assigned_provider": {
    "id": 1,
    "business_name": "Smith Plumbing Services"
  },
  ...
}
```

---

## Filtering & Search

### Global Filters (Available on Most Endpoints)

#### Search Filter
Use `search` parameter to search across multiple fields:
```http
GET /api/providers/?search=plumbing
GET /api/services/?search=leak repair
```

#### Ordering
Use `ordering` parameter (prefix with `-` for descending):
```http
GET /api/providers/?ordering=-average_rating
GET /api/services/?ordering=price
GET /api/bookings/?ordering=-created_at
```

#### Multiple Filters
Combine multiple filters:
```http
GET /api/services/?category=1&pricing_type=fixed&is_emergency_available=true&ordering=-created_at
```

### Pagination

**Query Parameters:**
- `page` - Page number (default: 1)
- `page_size` - Items per page (default: 20, max: 100)

**Example:**
```http
GET /api/services/?page=2&page_size=10
```

**Response includes:**
```json
{
  "count": 50,
  "next": "http://127.0.0.1:8000/api/services/?page=3",
  "previous": "http://127.0.0.1:8000/api/services/?page=1",
  "results": [...]
}
```

---

## Error Responses

### 400 Bad Request
```json
{
  "field_name": [
    "This field is required."
  ]
}
```

### 401 Unauthorized
```json
{
  "detail": "Authentication credentials were not provided."
}
```

### 403 Forbidden
```json
{
  "error": "Only the service provider can confirm bookings"
}
```

### 404 Not Found
```json
{
  "detail": "Not found."
}
```

### 500 Internal Server Error
```json
{
  "detail": "Internal server error"
}
```

---

## Rate Limiting

Currently no rate limiting is implemented. For production:
- Consider implementing throttling
- Use DRF's throttling classes
- Configure per-user and per-view limits

---

## Authentication Examples

### Login (Django Session Auth)
Use Django's built-in login:
```http
POST /admin/login/
```

Or implement custom login endpoint using Django auth

### Using Session in Requests
After login, session cookie is automatically included in subsequent requests.

---

## Webhooks (Future Enhancement)

Potential webhook events:
- `booking.confirmed`
- `booking.completed`
- `booking.cancelled`
- `review.created`
- `provider.verified`

---

## API Versioning

Current version: `v1` (implicit)

Future: Consider adding `/api/v1/` prefix for versioning

---

## Best Practices

1. **Always use HTTPS in production**
2. **Implement proper authentication** (Token/JWT for production)
3. **Validate all user inputs**
4. **Handle errors gracefully**
5. **Use pagination for large datasets**
6. **Cache frequently accessed data**
7. **Log API usage for monitoring**
8. **Implement rate limiting**
9. **Document all custom endpoints**
10. **Version your API**

---

**API Documentation Generated:** December 15, 2024  
**Version:** 1.0  
**Base URL:** `http://127.0.0.1:8000/api/`
