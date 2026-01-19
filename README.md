# 🏠 HomeServe - Home Services Marketplace

A comprehensive Django-based marketplace platform connecting homeowners with trusted service providers.

![Django](https://img.shields.io/badge/Django-5.2.8-green)
![DRF](https://img.shields.io/badge/DRF-3.16.1-red)
![Python](https://img.shields.io/badge/Python-3.12-blue)
![License](https://img.shields.io/badge/License-MIT-yellow)

## 🚀 Quick Start

```powershell
# Clone repository
cd c:\entry\frontend\django_folder\homeserve

# Activate virtual environment
..\my_virtual\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Start server
python manage.py runserver
```

**Access Points:**
- Admin Panel: `http://127.0.0.1:8000/admin/`
- API Root: `http://127.0.0.1:8000/api/`

## 📋 Features

### Core Functionality
✅ Multi-role system (Customers, Providers, Admin)  
✅ Service provider verification workflow  
✅ Advanced booking system with status tracking  
✅ Rating & review system with images  
✅ Emergency service request handling  
✅ Portfolio management for providers  
✅ Advanced search and filtering  
✅ REST API with full CRUD operations  

### Technical Highlights
✅ Django REST Framework integration  
✅ Custom admin panel with color-coded badges  
✅ Image upload and management  
✅ Automated rating calculations  
✅ Multi-status workflow management  
✅ CORS enabled for frontend integration  
✅ Pagination and filtering  

## 🛠️ Technology Stack

- **Backend:** Django 5.2.8
- **API:** Django REST Framework 3.16.1
- **Database:** SQLite (dev) / PostgreSQL (prod ready)
- **Authentication:** Session Authentication
- **Media Handling:** Pillow 12.0.0
- **Filtering:** django-filter 25.2
- **CORS:** django-cors-headers 4.9.0

## 📊 Database Models

### 7 Core Models:
1. **ServiceCategory** - Service classification
2. **ServiceProvider** - Provider profiles with verification
3. **Service** - Service offerings with pricing
4. **Booking** - Service bookings with workflow
5. **Review** - Customer reviews with ratings
6. **ProviderPortfolio** - Provider showcase
7. **ServiceRequest** - Emergency/custom requests

## 🔌 API Endpoints

### Main Routes:
- `/api/categories/` - Service categories
- `/api/providers/` - Service providers
- `/api/services/` - Available services
- `/api/bookings/` - Booking management
- `/api/reviews/` - Reviews & ratings
- `/api/portfolio/` - Provider portfolios
- `/api/service-requests/` - Service requests

**See [API_DOCUMENTATION.md](API_DOCUMENTATION.md) for complete API reference**

## 📖 Documentation

- **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)** - Comprehensive project overview
- **[SETUP_GUIDE.md](SETUP_GUIDE.md)** - Complete setup and testing guide
- **[API_DOCUMENTATION.md](API_DOCUMENTATION.md)** - Full API documentation

## 🎯 Use Cases

### For Customers:
- Browse service providers by category and location
- View provider profiles, ratings, and portfolios
- Book services with preferred date/time
- Track booking status in real-time
- Leave reviews and ratings after service completion
- Create emergency service requests

### For Service Providers:
- Register and create business profile
- List multiple services with pricing
- Manage availability and working hours
- Accept/reject booking requests
- Build portfolio with project photos
- Respond to customer reviews
- View booking history and analytics

### For Administrators:
- Verify service provider credentials
- Manage service categories
- Monitor all bookings and transactions
- Handle disputes and cancellations
- View platform analytics
- Manage user accounts

## 🎨 Admin Panel Features

- **Color-coded status badges** for quick visualization
- **Advanced filtering** by multiple criteria
- **Bulk actions** for efficiency (verify providers, confirm bookings)
- **Custom admin actions** with workflow automation
- **Inline editing** for related models
- **Search functionality** across multiple fields
- **Date hierarchy** for time-based filtering
- **Readonly fields** for calculated data

## 🔒 Security Features

- User authentication and authorization
- Provider verification system
- CSRF protection
- SQL injection prevention (Django ORM)
- XSS protection
- Secure password hashing
- Session management

## 📈 Scalability Considerations

**Ready for:**
- Frontend integration (React, Vue, Mobile apps)
- Payment gateway integration (Stripe, PayPal)
- Real-time notifications (WebSocket)
- Geolocation services (Google Maps)
- Email/SMS notifications
- Advanced analytics
- Multi-language support

**Deployment Options:**
- PythonAnywhere
- Heroku
- AWS/Azure/GCP
- DigitalOcean
- Docker containerization

## 🧪 Testing

### Admin Panel Testing:
```powershell
# Create superuser
python manage.py createsuperuser

# Access admin
http://127.0.0.1:8000/admin/
```

### API Testing:
```powershell
# Test GET endpoint
curl http://127.0.0.1:8000/api/services/

# Test with filters
curl "http://127.0.0.1:8000/api/services/?category=1&is_emergency_available=true"
```

**See [SETUP_GUIDE.md](SETUP_GUIDE.md) for detailed testing instructions**

## 📦 Project Structure

```
homeserve/
├── manage.py
├── requirements.txt
├── README.md
├── PROJECT_SUMMARY.md
├── SETUP_GUIDE.md
├── API_DOCUMENTATION.md
├── db.sqlite3
├── homeserve/
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── services/
│   ├── models.py          # 7 database models
│   ├── admin.py           # Custom admin panels
│   ├── serializers.py     # DRF serializers
│   ├── views.py           # API ViewSets
│   ├── urls.py            # URL routing
│   └── migrations/
└── media/                 # User uploads
    ├── providers/
    ├── services/
    ├── reviews/
    ├── portfolio/
    └── verification_docs/
```

## 🎓 Learning Outcomes

This project demonstrates proficiency in:
- RESTful API design and implementation
- Complex database modeling and relationships
- Django admin customization
- Business logic implementation
- User authentication and authorization
- File upload and media handling
- Query optimization
- Code organization and best practices

## 🌟 Resume Highlights

**Key Achievements:**
- Built a two-sided marketplace with 7 interconnected models
- Implemented provider verification workflow with 3-stage approval
- Created automated rating system with real-time updates
- Designed flexible booking system handling 6 status states
- Developed 40+ REST API endpoints with advanced filtering
- Customized admin interface with color-coded visual indicators

**Interview Talking Points:**
- "Designed a scalable marketplace connecting service providers with customers"
- "Implemented complex workflow management for bookings and verifications"
- "Built a smart rating algorithm that automatically updates provider rankings"
- "Created a comprehensive REST API ready for mobile/web frontend integration"
- "Developed an emergency request system for urgent service needs"

## 🚧 Future Enhancements

### Phase 2 Features:
- [ ] Payment gateway integration
- [ ] Real-time chat system
- [ ] Google Maps integration for location-based services
- [ ] Email/SMS notifications
- [ ] Advanced analytics dashboard
- [ ] Service provider availability calendar
- [ ] Mobile app (React Native)
- [ ] Customer loyalty program
- [ ] Multi-language support

### Performance Optimizations:
- [ ] Redis caching
- [ ] Celery for background tasks
- [ ] Elasticsearch for advanced search
- [ ] CDN for media files
- [ ] Database query optimization
- [ ] API response caching

## 📄 License

MIT License - Feel free to use for learning and portfolio purposes



## 🙏 Acknowledgments

- Django Documentation
- Django REST Framework Documentation
- Stack Overflow Community

---

**⭐ If you find this project helpful, please give it a star!**

**📧 Questions? Feel free to reach out!**

---

**Project Status:** ✅ Production Ready  
**Last Updated:** December 15, 2024  
**Version:** 1.0.0
