# KilometriTracker - Business Travel Distance Tracking API

A Django REST Framework API for tracking business travel distances with automatic Google Maps integration and manual entry options. Generates monthly reports with Excel/PDF export for accounting purposes.

**Built by:** CodeNob Dev (Anti-Vibe Coding)
**Author:** Sami Tommilammi
**Tech Stack:** Django 4.2, DRF, PostgreSQL, JWT, Celery, Google Maps API
**Security:** Rate limiting, input validation, JWT authentication, permission checks
# KilometriTracker - Business Travel Distance Tracking API

A Django REST Framework API for tracking business travel distances with automatic Google Maps integration and manual entry options. Generates monthly reports with **professional PDF export** for accounting purposes.

**Built by:** CodeNob Dev (Anti-Vibe Coding)
**Author:** Sami Tommilammi
**Tech Stack:** Django 4.2, DRF, PostgreSQL, JWT, ReportLab
**Security:** Rate limiting, input validation, JWT authentication, permission checks
**Status:** ✅ MVP Complete - Backend 100% functional

---

## 🎯 Project Overview

KilometriTracker is a full-featured REST API for business travel tracking that allows users to:
- Track business trips with automatic distance calculation (Google Maps)
- Manually enter trip data when needed
- Generate monthly travel reports
- **Export reports to PDF with professional formatting** ✅ **NEW!**
- Export data to Excel (future feature)
- Receive automated monthly summaries via email (future feature)

### Key Features

✅ **User Management**
- User registration with JWT token generation
- Secure login/logout with token blacklisting
- Profile management
- Password change with old password verification

✅ **Trip Tracking**
- Manual trip entry (date, addresses, distance, purpose)
- Google Maps Distance Matrix API integration (placeholder)
- Trip CRUD operations (Create, Read, Update, Delete)
- Advanced filtering and search
- Monthly summaries

✅ **Monthly Reports** ⭐ **UPDATED!**
- Automatic report generation
- Trip statistics (total km, trip count)
- **Professional PDF export with ReportLab** ✅
- Excel export (planned)
- Email delivery (planned)

✅ **PDF Report Features** 🆕
- Professional A4 layout with branding
- User information section (name, company, email)
- Formatted trip table (date, from, to, distance, purpose)
- Summary section (total trips, total kilometers)
- Generation timestamp
- Color-coded design (#3498DB headers, alternating rows)
- Automatic file storage in `media/reports/pdf/`
- PDF URL returned in API response for direct download

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
- Google Maps Distance Matrix API (distance calculation - placeholder)
- Celery + Redis (scheduled tasks - future)

**Security & Rate Limiting:**
- django-ratelimit 4.1.0
- django-cors-headers 4.3.1

**Report Generation:** ⭐ **UPDATED!**
- **reportlab 4.0.9 (PDF generation)** ✅ **IMPLEMENTED!**
- openpyxl 3.1.2 (Excel files - future)

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
│   ├── reports/            # Monthly reports ⭐ UPDATED!
│   │   ├── models.py       # MonthlyReport model
│   │   ├── serializers.py  # Report serialization
│   │   ├── views.py        # Report endpoints
│   │   ├── generators.py   # 🆕 PDF generation with ReportLab
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
├── media/                  # User uploads ⭐ UPDATED!
│   └── reports/
│       └── pdf/            # 🆕 Generated PDF reports
├── static/                 # Static files
├── db.sqlite3              # Database (development)
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables
├── .gitignore              # Git ignore rules
├── README.md               # This file
├── TESTING_GUIDE.md        # 🆕 Comprehensive API testing guide
└── QUICK_REFERENCE.md      # 🆕 Quick curl command reference
```

---

## 🚀 Installation & Setup

### Prerequisites

- Python 3.12+
- pip (Python package manager)
- Git
- Google Maps API key (for distance calculation - optional for MVP)

### 1. Clone Repository
```bash
git clone https://github.com/Xmas178/KilometriTracker.git
cd KilometriTracker/backend
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

# Google Maps API (optional for MVP)
GOOGLE_MAPS_API_KEY=your-google-maps-api-key

# Email (console backend for dev)
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend

# CORS - Update for frontend
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000,http://localhost:5173
```

### 5. Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create Superuser
```bash
python manage.py createsuperuser
# Username: admin
# Password: salasana1234 (development only!)
```

### 7. Run Development Server
```bash
python manage.py runserver
```

API is now available at: `http://127.0.0.1:8000/`
Admin panel: `http://127.0.0.1:8000/admin/`

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

#### Authentication & Users (8 endpoints)

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

#### Trips (5 endpoints)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/trips/` | List all trips | Yes |
| POST | `/api/trips/` | Create new trip | Yes |
| GET | `/api/trips/<id>/` | View trip details | Yes (Owner) |
| PUT/PATCH | `/api/trips/<id>/` | Update trip | Yes (Owner) |
| DELETE | `/api/trips/<id>/` | Delete trip | Yes (Owner) |
| POST | `/api/trips/calculate-distance/` | Calculate distance (Google Maps) | Yes |
| GET | `/api/trips/monthly-summary/` | Get monthly summary | Yes |

#### Reports (3 endpoints) ⭐ **UPDATED!**

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/reports/` | List all reports | Yes |
| GET | `/api/reports/<id>/` | View report details | Yes (Owner) |
| POST | `/api/reports/generate/` | **Generate monthly report + PDF** ✅ | Yes |

**Total: 16 fully functional API endpoints**

---

## 🆕 PDF Report Generation

### How It Works

When you generate a monthly report via `POST /api/reports/generate/`, the system automatically:

1. Creates a `MonthlyReport` database record
2. Fetches all trips for the specified month
3. Generates a professional PDF using ReportLab
4. Saves the PDF to `media/reports/pdf/report_{username}_{year}_{month}.pdf`
5. Returns the PDF URL in the API response

### PDF Features

**Layout:**
- A4 page size (210mm × 297mm)
- Professional margins (2cm all sides)
- Custom color scheme (Blue headers: #3498DB, Dark text: #2C3E50)

**Content Sections:**
1. **Title:** "Travel Report - [Month Year]"
2. **User Info:** Name, Company, Email
3. **Trip Table:**
   - Columns: Date | From | To | Distance (km) | Purpose
   - Blue header row
   - Alternating row colors (white/light gray)
   - Grid borders for readability
   - Address truncation (max 30 chars)
   - Right-aligned distances
4. **Summary:**
   - Total Trips count
   - Total Distance in km
5. **Footer:** Generation timestamp

### Example Request

```bash
POST /api/reports/generate/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "year": 2025,
  "month": 11
}
```

### Example Response

```json
{
  "id": 1,
  "user": 3,
  "user_display": "Test User",
  "year": 2025,
  "month": 11,
  "period_display": "November 2025",
  "total_km": "165.50",
  "trip_count": 1,
  "pdf_url": "http://127.0.0.1:8000/media/reports/pdf/report_testuser_2025_11_xxx.pdf",
  "excel_url": null,
  "sent_at": null,
  "created_at": "2025-12-08T16:31:00.123456Z"
}
```

### Accessing the PDF

**Option 1:** Direct browser access
```
http://127.0.0.1:8000/media/reports/pdf/report_testuser_2025_11_xxx.pdf
```

**Option 2:** Download via curl
```bash
curl -o report.pdf "http://127.0.0.1:8000/media/reports/pdf/report_testuser_2025_11_xxx.pdf"
```

**Option 3:** Frontend integration
```javascript
// Get PDF URL from API response
const response = await axios.post('/api/reports/generate/', { year: 2025, month: 11 });
const pdfUrl = response.data.pdf_url;

// Open in new tab or trigger download
window.open(pdfUrl, '_blank');
```

---

## 📖 Additional Documentation

For detailed API testing examples and command references, see:

- **[TESTING_GUIDE.md](TESTING_GUIDE.md)** - Comprehensive API testing guide with curl examples
- **[QUICK_REFERENCE.md](QUICK_REFERENCE.md)** - Quick copy-paste curl commands

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

### Manual API Testing

All endpoints have been tested with curl commands. See [TESTING_GUIDE.md](TESTING_GUIDE.md) for examples.

**Quick test:**
```bash
# 1. Register user
curl -X POST http://127.0.0.1:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "salasana123",
    "password2": "salasana123"
  }'

# 2. Save access token from response, then create a trip
curl -X POST http://127.0.0.1:8000/api/trips/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "date": "2025-11-15",
    "start_address": "Tampere, Finland",
    "end_address": "Turku, Finland",
    "distance_km": 165.5,
    "purpose": "Client visit",
    "is_manual": true
  }'

# 3. Generate PDF report
curl -X POST http://127.0.0.1:8000/api/reports/generate/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"year": 2025, "month": 11}'
```

### Automated Tests (Future)
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

### Production Checklist

- [ ] Set `DEBUG=False` in settings
- [ ] Configure PostgreSQL database
- [ ] Set strong `SECRET_KEY`
- [ ] Configure ALLOWED_HOSTS
- [ ] Set up Redis for Celery (future)
- [ ] Configure email backend (SMTP)
- [ ] Set up nginx for static/media files
- [ ] Enable HTTPS (SSL certificates)
- [ ] Configure proper CORS origins
- [ ] Set up monitoring and logging
- [ ] Run collectstatic
- [ ] Set up automated backups
- [ ] Configure media file storage (AWS S3, etc.)

### Docker Setup (Future)
```bash
docker-compose up -d
```

---

## 💡 Current Status & Roadmap

### ✅ Completed Features (MVP)

- [x] User registration and authentication (JWT)
- [x] Trip CRUD operations
- [x] Monthly summaries
- [x] Report generation
- [x] **Professional PDF export with ReportLab** 🆕
- [x] Rate limiting
- [x] Input validation
- [x] Permission-based access control
- [x] Comprehensive API documentation
- [x] Testing guides

### 🚧 In Progress

- [ ] **Frontend (React + Mantine + Vite)** ← Next priority
  - Login/Register pages
  - Trip list with Add/Edit/Delete
  - **"Generate & Download PDF" button**
  - Dashboard with statistics
  - Responsive mobile design

### 📅 Future Enhancements

1. **Excel Report Generation**
   - Professional Excel exports with formulas
   - Multiple worksheets (summary, trips, statistics)
   - Email delivery of reports

2. **Automated Monthly Reports**
   - Celery scheduled tasks
   - Automatic report generation at month-end
   - Email notifications with PDF attachments

3. **Google Maps Integration**
   - Full Distance Matrix API integration (requires API key)
   - Route caching to reduce API costs
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

6. **Testing & CI/CD**
   - Unit tests with pytest
   - Integration tests
   - Docker containerization
   - GitHub Actions CI/CD pipeline

---

## 📝 Notes & Considerations

### Google Maps API Costs

**Current Implementation:**
- Google Maps Distance Matrix API is included as placeholder
- Requires API key activation (not critical for MVP)
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

### PDF Generation Performance

- PDF generation is fast (<1 second for typical reports)
- Files are stored in `media/reports/pdf/` directory
- Consider cloud storage (AWS S3) for production
- Implement cleanup job for old reports (>1 year)

### File Upload Validator

The `validate_file_size()` function in `apps/core/validators.py` is included for future features (receipt uploads, bulk import) but is not currently used in MVP.

---

## 👨‍💻 Development

### Code Style

- **Language:** English comments and documentation (CodeNob Dev style)
- **Formatting:** Black (line length 100)
- **Linting:** Flake8
- **Type Hints:** Encouraged, checked with mypy
- **Commits:** Descriptive messages in English

### Git Workflow
```bash
# Create feature branch
git checkout -b feature/excel-export

# Make changes and commit
git add .
git commit -m "Add Excel export functionality"

# Push to remote
git push origin feature/excel-export
```

### Recent Commits
```bash
# Latest features
✅ Fix reports serializer bug and add API testing documentation
✅ Add PDF report generation feature with ReportLab
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
**Project Repository:** https://github.com/Xmas178/KilometriTracker

---

## 🙏 Acknowledgments

- Django REST Framework documentation
- ReportLab documentation
- Google Maps API documentation
- CodeNob Dev "Anti-Vibe Coding" principles

---

**Backend Status:** ✅ MVP Complete - Ready for frontend development
**Last Updated:** December 8, 2025
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
```bashgit push -u origin main

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
## Frontend Integration

### CORS Configuration

Frontend runs on http://localhost:5173 (Vite default port).

Ensure `.env` contains:
```
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000,http://localhost:5173,http://127.0.0.1:5173
```

### API Response Format

**Authentication endpoints return:**
```json
{
  "user": {
    "id": 1,
    "username": "testuser",
    "email": "test@example.com",
    ...
  },
  "tokens": {
    "access": "eyJhbGc...",
    "refresh": "eyJhbGc..."
  },
  "message": "User registered successfully"
}
```

**Trip validation:**
- Address fields: Minimum 1 character (changed from 5 for abbreviations like "HKI", "TRE")
- Distance: Must be positive number
- Date: ISO format (YYYY-MM-DD)

### Testing with Frontend

1. Start backend: `python manage.py runserver`
2. Start frontend: `npm run dev` (in frontend directory)
3. Frontend available at: http://localhost:5173
4. Register with test user:
   - Username: `testuser`
   - Password: `salasana123`
5. Login with test user


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
- CodeNob Dev "Anti-Vibe Coding" principlescode /home/crake178/projects/kilometri-tracker/backend/README.md