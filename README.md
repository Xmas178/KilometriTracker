# KilometriTracker - Business Travel Distance Tracking API

A Django REST Framework API for tracking business travel distances with automatic Google Maps integration and manual entry options. Generates monthly reports with Excel/PDF export for accounting purposes.

**Built by:** CodeNob Dev (Anti-Vibe Coding)
**Author:** Sami Lammi
**Tech Stack:** Django 4.2, DRF, PostgreSQL, JWT, Celery, Google Maps API
**Security:** Rate limiting, input validation, JWT authentication, permission checks

---

## 🎯 Project Overview

KilometriTracker is a full-featured REST API for business travel tracking that allows users to:
- Track business trips with automatic distance calculation (Google Maps)
- Manually enter trip data when needed
- Generate monthly travel reports
- Export data to Excel and PDF (future feature)
- Receive automated monthly summaries via email (future feature)

### Key Features

✅ **User Management**
- User registration with JWT token generation
- Secure login/logout with token blacklisting
- Profile management
- Password change with old password verification

✅ **Trip Tracking**
- Manual trip entry (date, addresses, distance, purpose)
- Google Maps Distance Matrix API integration
- Trip CRUD operations (Create, Read, Update, Delete)
- Advanced filtering and search
- Monthly summaries

✅ **Monthly Reports**
- Automatic report generation
- Trip statistics (total km, trip count)
- PDF/Excel export (planned)
- Email delivery (planned)

✅ **Security & Validation**
- Rate limiting on sensitive endpoints
- Input validation (addresses, distances, dates)
- SQL injection & XSS prevention
- JWT authentication with token rotation
- Permission-based access control

---

## 🏗️ Architecture

### Tech Stack

**Backend Framework:**
- Django 4.2.9 (Python web framework)
- Django REST Framework 3.14.0 (API toolkit)
- djangorestframework-simplejwt 5.3.1 (JWT authentication)

**Database:**
- SQLite (development)
- PostgreSQL (production-ready)

**APIs & Services:**
- Google Maps Distance Matrix API (distance calculation)
- Celery + Redis (scheduled tasks - future)

**Security & Rate Limiting:**
- django-ratelimit 4.1.0
- django-cors-headers 4.3.1

**Report Generation:**
- openpyxl 3.1.2 (Excel files)
- reportlab 4.0.9 (PDF files)

**Testing & Quality:**
- pytest 7.4.4
- pytest-django 4.7.0
- pytest-cov 4.1.0 (coverage reports)
- black 24.1.1 (code formatting)
- flake8 7.0.0 (linting)
- mypy 1.8.0 (type checking)

### Project Structure
```
backend/
├── apps/
│   ├── users/              # User management & authentication
│   │   ├── models.py       # Custom User model
│   │   ├── serializers.py  # User serialization
│   │   ├── views.py        # Auth endpoints
│   │   └── urls.py         # User routes
│   │
│   ├── trips/              # Trip tracking
│   │   ├── models.py       # Trip model
│   │   ├── serializers.py  # Trip serialization
│   │   ├── views.py        # CRUD endpoints
│   │   ├── services.py     # Google Maps integration
│   │   └── urls.py         # Trip routes
│   │
│   ├── reports/            # Monthly reports
│   │   ├── models.py       # MonthlyReport model
│   │   ├── serializers.py  # Report serialization
│   │   ├── views.py        # Report endpoints
│   │   └── urls.py         # Report routes
│   │
│   └── core/               # Shared utilities
│       ├── exceptions.py   # Custom exceptions
│       ├── validators.py   # Input validation
│       └── permissions.py  # Access control
│
├── config/                 # Django settings
│   ├── settings.py         # Main configuration
│   ├── urls.py             # Root URL routing
│   └── wsgi.py             # WSGI application
│
├── media/                  # User uploads (PDF/Excel)
├── static/                 # Static files
├── db.sqlite3              # Database (development)
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables
├── .gitignore              # Git ignore rules
└── README.md               # This file
```

---

## 🚀 Installation & Setup

### Prerequisites

- Python 3.12+
- pip (Python package manager)
- Git
- Google Maps API key (for distance calculation)

### 1. Clone Repository
```bash
git clone <repository-url>
cd kilometri-tracker/backend
```

### 2. Create Virtual Environment
```bash
python3.12 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create `.env` file:
```bash
cp .env.example .env
```

Edit `.env` and configure:
```bash
# Django
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (SQLite for dev, PostgreSQL for production)
# DATABASE_URL=postgresql://user:password@localhost:5432/dbname

# Google Maps API
GOOGLE_MAPS_API_KEY=your-google-maps-api-key

# Email (console backend for dev)
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend

# CORS
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

### 5. Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create Superuser
```bash
python manage.py createsuperuser
```

### 7. Run Development Server
```bash
python manage.py runserver
```

API is now available at: `http://127.0.0.1:8000/`

---

## 📚 API Documentation

### Base URL

Development: `http://127.0.0.1:8000/api/`

### Authentication

All endpoints (except registration and login) require JWT authentication.

**Header format:**
```
Authorization: Bearer <access_token>
```

### Endpoints Overview

#### Authentication & Users

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/auth/register/` | Register new user | No |
| POST | `/api/auth/login/` | Login (get JWT tokens) | No |
| POST | `/api/auth/logout/` | Logout (blacklist token) | Yes |
| POST | `/api/auth/token/refresh/` | Refresh access token | No |
| POST | `/api/auth/change-password/` | Change password | Yes |
| GET | `/api/auth/profile/` | View own profile | Yes |
| PUT/PATCH | `/api/auth/profile/` | Update own profile | Yes |
| GET | `/api/users/` | List all users (admin) | Yes (Admin) |
| GET | `/api/users/<id>/` | View user details | Yes (Self/Admin) |

#### Trips

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/trips/` | List all trips | Yes |
| POST | `/api/trips/` | Create new trip | Yes |
| GET | `/api/trips/<id>/` | View trip details | Yes (Owner) |
| PUT/PATCH | `/api/trips/<id>/` | Update trip | Yes (Owner) |
| DELETE | `/api/trips/<id>/` | Delete trip | Yes (Owner) |
| POST | `/api/trips/calculate-distance/` | Calculate distance (Google Maps) | Yes |
| GET | `/api/trips/monthly-summary/` | Get monthly summary | Yes |

#### Reports

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/reports/` | List all reports | Yes |
| GET | `/api/reports/<id>/` | View report details | Yes (Owner) |
| POST | `/api/reports/generate/` | Generate monthly report | Yes |

### Example Requests

#### Register New User
```bash
POST /api/auth/register/
Content-Type: application/json

{
  "username": "sami",
  "email": "sami@example.com",
  "password": "securepass123",
  "password2": "securepass123",
  "first_name": "Sami",
  "last_name": "Lammi",
  "company": "CodeNob Dev"
}
```

**Response (201 Created):**
```json
{
  "user": {
    "id": 1,
    "username": "sami",
    "email": "sami@example.com",
    "first_name": "Sami",
    "last_name": "Lammi",
    "company": "CodeNob Dev",
    "created_at": "2025-12-06T20:00:00Z"
  },
  "tokens": {
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
  },
  "message": "User registered successfully"
}
```

#### Create Trip (Manual Entry)
```bash
POST /api/trips/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "date": "2025-12-06",
  "start_address": "Oulu, Finland",
  "end_address": "Helsinki, Finland",
  "distance_km": 607.5,
  "purpose": "Business meeting",
  "is_manual": true
}
```

#### Calculate Distance (Google Maps)
```bash
POST /api/trips/calculate-distance/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "start_address": "Oulu, Finland",
  "end_address": "Helsinki, Finland"
}
```

**Response (200 OK):**
```json
{
  "distance_km": 607.5,
  "distance_meters": 607500,
  "duration_seconds": 21600,
  "start_address": "Oulu, Finland",
  "end_address": "Helsinki, Finland",
  "route_data": {...}
}
```

#### Generate Monthly Report
```bash
POST /api/reports/generate/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "year": 2025,
  "month": 12
}
```

---

## 🔒 Security Features

### Rate Limiting

| Endpoint | Limit | Key |
|----------|-------|-----|
| `/api/auth/register/` | 3 requests/hour | IP address |
| `/api/auth/change-password/` | 3 requests/15 min | User |
| `/api/auth/logout/` | 10 requests/min | User |
| `/api/trips/calculate-distance/` | 30 requests/min | User |

### Input Validation

- **Addresses:** Min 5 chars, max 500 chars, XSS/SQL injection prevention
- **Distances:** Positive numbers, 0.01-9999.99 km range
- **Dates:** Not in future, not older than 2 years
- **Passwords:** Min 8 chars, Django validators (common passwords, similarity checks)

### Authentication & Authorization

- **JWT Tokens:** 1-hour access tokens, 7-day refresh tokens
- **Token Rotation:** New refresh token issued on refresh
- **Token Blacklisting:** Logout invalidates refresh token
- **Permissions:** Users can only access their own data

---

## 🧪 Testing

### Run Tests
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=apps --cov-report=html

# Run specific app tests
pytest apps/users/tests/
pytest apps/trips/tests/
```

### Code Quality
```bash
# Format code
black apps/

# Lint code
flake8 apps/ --max-line-length=100

# Type checking
mypy apps/ --ignore-missing-imports
```

---

## 🚀 Deployment

### Docker Setup (Coming Soon)
```bash
docker-compose up -d
```

### Production Checklist

- [ ] Set `DEBUG=False` in settings
- [ ] Configure PostgreSQL database
- [ ] Set strong `SECRET_KEY`
- [ ] Configure ALLOWED_HOSTS
- [ ] Set up Redis for Celery
- [ ] Configure email backend (SMTP)
- [ ] Set up nginx for static/media files
- [ ] Enable HTTPS (SSL certificates)
- [ ] Configure proper CORS origins
- [ ] Set up monitoring and logging
- [ ] Run collectstatic
- [ ] Set up automated backups

---

## 💡 Future Features

### Planned Enhancements

1. **PDF/Excel Report Generation**
   - Professional PDF reports with charts
   - Excel exports with formulas
   - Email delivery of reports

2. **Automated Monthly Reports**
   - Celery scheduled tasks
   - Automatic report generation at month-end
   - Email notifications

3. **Google Maps Integration Improvements**
   - Route caching to reduce API costs
   - Optional premium feature (pay-per-use)
   - Support for multiple transportation modes

4. **Enhanced Features**
   - Multi-vehicle support
   - Fuel cost tracking
   - CO2 emissions calculation
   - Team/company accounts
   - Admin dashboard
   - Mobile app API support

5. **Internationalization**
   - Finnish language support
   - Multi-language interface
   - Currency/unit conversions

---

## 📝 Notes & Considerations

### Google Maps API Costs

**Current Implementation:**
- Google Maps Distance Matrix API is included for demo/MVP
- Cost: ~$5 per 1000 requests

**Production Recommendations:**
- Make Google Maps optional or premium-only feature
- Default to manual entry (free)
- Cache common routes
- Consider rate limiting per user tier

**Estimated Costs:**
- 100 users × 10 trips/month = 1000 requests = $5/month
- 1000 users = $50/month
- 10,000 users = $500/month

### File Upload Validator

The `validate_file_size()` function in `apps/core/validators.py` is included for future features (receipt uploads, bulk import) but is not currently used in MVP.

---

## 👨‍💻 Development

### Code Style

- **Language:** English comments and documentation (CodeNob Dev style)
- **Formatting:** Black (line length 100)
- **Linting:** Flake8
- **Type Hints:** Encouraged, checked with mypy

### Git Workflow
```bash
# Create feature branch
git checkout -b feature/trip-analytics

# Make changes and commit
git add .
git commit -m "Add trip analytics endpoint"

# Push to remote
git push origin feature/trip-analytics
```

---

## 📄 License

This project is part of CodeNob Dev portfolio.

---

## 🤝 Contact

**Developer:** Sami Tommilammi
**Company:** CodeNob Dev
**Portfolio:** www.tommilammi.fi
**GitHub:** https://github.com/Xmas178

---

## 🙏 Acknowledgments

- Django REST Framework documentation
- Google Maps API documentation
- CodeNob Dev "Anti-Vibe Coding" principles