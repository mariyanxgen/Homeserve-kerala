# HomeServe Kerala - Frontend

## 🎨 Kerala-Themed HTML Frontend

A beautiful, responsive HTML/CSS/JavaScript frontend for HomeServe marketplace, specifically designed for Kerala with:
- **Kerala color scheme** (Green & Gold)
- **Malayalam language support** (Bilingual UI)
- **All 14 Kerala districts** integrated
- **Pure HTML/CSS/JS** - No build tools required!

---

## 🚀 Quick Start

### 1. Start Django Backend
```powershell
cd c:\entry\frontend\django_folder\homeserve
python manage.py runserver
```

### 2. Open Frontend
Simply open `index.html` in your browser:
```powershell
# Option 1: Double-click index.html

# Option 2: Use Live Server (VS Code extension)
# Right-click on index.html → Open with Live Server

# Option 3: Python simple server
cd frontend
python -m http.server 8080
# Then open: http://localhost:8080
```

### 3. Configure CORS (Important!)
The Django backend is already configured for CORS, but ensure `settings.py` has:
```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:8080",
    "http://127.0.0.1:8080",
    "http://localhost:5500",  # Live Server default
]
```

---

## 📁 Project Structure

```
frontend/
├── index.html              # Homepage
├── services.html           # Browse all services
├── providers.html          # Service providers list
├── bookings.html           # User bookings
├── about.html              # About page
├── css/
│   └── style.css          # Kerala-themed styles
├── js/
│   ├── api.js             # API service layer
│   ├── main.js            # Core functionality
│   └── services.js        # Services page logic
└── images/                 # Images (add your own)
```

---

## 🎨 Features

### Kerala-Specific Features
✅ All 14 Kerala districts in filters  
✅ Malayalam language support (ഹോംസെർവ് കേരള)  
✅ Kerala color scheme (Green & Gold)  
✅ "God's Own Services" tagline  
✅ Cultural design elements  

### Functional Features
✅ Browse services by category/district  
✅ Search functionality  
✅ Filter by price, type, location  
✅ Emergency services badge  
✅ Provider profiles with ratings  
✅ Responsive mobile design  
✅ Real-time API integration  

---

## 🌍 Kerala Districts Supported

All 14 districts are integrated:
1. Thiruvananthapuram (തിരുവനന്തപുരം)
2. Kollam (കൊല്ലം)
3. Pathanamthitta (പത്തനംതിട്ട)
4. Alappuzha (ആലപ്പുഴ)
5. Kottayam (കോട്ടയം)
6. Idukki (ഇടുക്കി)
7. Ernakulam (എറണാകുളം)
8. Thrissur (തൃശ്ശൂർ)
9. Palakkad (പാലക്കാട്)
10. Malappuram (മലപ്പുറം)
11. Kozhikode (കോഴിക്കോട്)
12. Wayanad (വയനാട്)
13. Kannur (കണ്ണൂർ)
14. Kasaragod (കാസർഗോഡ്)

---

## 🔌 API Integration

### API Base URL
```javascript
const API_BASE_URL = 'http://127.0.0.1:8000/api';
```

### Available Endpoints
The frontend connects to:
- `/api/categories/` - Service categories
- `/api/providers/` - Service providers
- `/api/services/` - All services
- `/api/services/search/` - Advanced search
- `/api/bookings/` - User bookings
- `/api/reviews/` - Reviews & ratings

### Making API Calls
```javascript
// Example: Get all services
const services = await api.getServices();

// Example: Search services
const results = await api.searchServices('plumbing', { city: 'Kochi' });

// Example: Get providers by district
const providers = await api.getProviders({ city: 'Thiruvananthapuram' });
```

---

## 🎨 Color Palette

Kerala-inspired colors:
```css
--kerala-green: #006838     /* Primary brand color */
--kerala-gold: #FFD700      /* Accent color */
--kerala-red: #DC143C       /* Emergency/Alert */
--kerala-light-green: #90EE90 /* Success states */
```

---

## 📱 Pages Overview

### 1. Homepage (`index.html`)
- Hero section with search
- Popular services grid
- Featured providers
- How it works section
- All 14 districts showcase
- Statistics section

### 2. Services Page (`services.html`)
- Advanced filters (district, category, price, type)
- Search functionality
- Sort options
- Service cards with pricing
- Emergency badge indicators

### 3. Providers Page (`providers.html`)
- Provider listings
- Ratings & reviews
- District-wise filtering
- Verified badges

### 4. Bookings Page (`bookings.html`)
- User booking history
- Booking status tracking
- Cancel/modify options

### 5. About Page (`about.html`)
- Company information
- Contact details
- Service areas (Kerala districts)

---

## 🛠️ Customization

### Change Colors
Edit `css/style.css`:
```css
:root {
    --kerala-green: #YOUR_COLOR;
    --kerala-gold: #YOUR_COLOR;
}
```

### Add More Districts/Cities
Edit `js/main.js`:
```javascript
const KERALA_DISTRICTS = [
    'Thiruvananthapuram',
    // Add more...
];
```

### Change API URL
Edit `js/api.js`:
```javascript
const API_BASE_URL = 'https://your-domain.com/api';
```

---

## 🌐 Deployment

### Option 1: Static Hosting
Upload `frontend/` folder to:
- GitHub Pages
- Netlify
- Vercel
- Firebase Hosting

### Option 2: With Django
Add to Django's `urls.py`:
```python
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # ... your URLs
] + static('/frontend/', document_root=settings.BASE_DIR / 'frontend')
```

Then access at: `http://127.0.0.1:8000/frontend/`

---

## 🔧 Troubleshooting

### CORS Errors
Ensure Django settings has:
```python
INSTALLED_APPS = [
    ...
    'corsheaders',
]

MIDDLEWARE = [
    ...
    'corsheaders.middleware.CorsMiddleware',
]

CORS_ALLOW_ALL_ORIGINS = True  # For development only
```

### API Not Loading
1. Check Django server is running: `http://127.0.0.1:8000/api/`
2. Check browser console for errors (F12)
3. Verify API_BASE_URL in `js/api.js`

### Malayalam Text Not Showing
Add to HTML `<head>`:
```html
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+Malayalam&display=swap" rel="stylesheet">
```

---

## 📸 Screenshots

Take screenshots for:
- Homepage hero section
- Services grid with filters
- Provider profiles
- Booking interface
- Mobile responsive views

---

## 🎓 Learning Points

This frontend demonstrates:
- ✅ Vanilla JavaScript (no frameworks)
- ✅ Fetch API for backend integration
- ✅ CSS Grid & Flexbox layouts
- ✅ Responsive design principles
- ✅ Kerala cultural integration
- ✅ Bilingual UI (English/Malayalam)
- ✅ User-friendly search & filters
- ✅ Professional color schemes

---

## 🚀 Future Enhancements

- [ ] User authentication UI
- [ ] Booking form with date/time picker
- [ ] Payment integration UI
- [ ] Real-time notifications
- [ ] Chat widget
- [ ] Advanced search filters
- [ ] Provider dashboard
- [ ] Customer reviews with images
- [ ] Map integration (Google Maps)
- [ ] Progressive Web App (PWA)

---

## 📄 License

MIT License - Use freely for learning and portfolio

---

## 👨‍💻 Developer Notes

**Tech Stack:**
- HTML5
- CSS3 (Grid, Flexbox, Animations)
- Vanilla JavaScript (ES6+)
- Fetch API
- Font Awesome Icons

**Browser Support:**
- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)
- Mobile browsers

**No Dependencies:**
- No npm/node required
- No build process
- No bundlers
- Pure web technologies

---

**Made with ❤️ for God's Own Country - Kerala**

**🏠 HomeServe കേരള - Connecting Kerala homes with trusted services**
