## Docker

### Build Docker Image
```bash
docker build -t kilometri-backend .
```

### Run Container
```bash
docker run -p 8000:8000 \
  -e DATABASE_URL=postgresql://user:pass@host:5432/db \
  -e SECRET_KEY=your-secret-key \
  kilometri-backend
```

### Docker Compose

Full stack with PostgreSQL and frontend:
```bash
# From fullstack directory
docker-compose up

# Backend available at: http://localhost:8000/
# Frontend available at: http://localhost/
```

## CI/CD

GitHub Actions workflow runs automatically on push to main:

1. Checkout code
2. Setup Python 3.12
3. Install dependencies
4. Setup PostgreSQL service (test database)
5. Run Django checks
6. Run migrations
7. Run tests (if exist)
8. Security scan with safety
9. Build Docker image
10. Verify Docker image

Pipeline status: https://github.com/Xmas178/kilometri-tracker/actions

## Frontend Integration

### CORS Configuration

Frontend runs on http://localhost:5173 (Vite) or http://localhost (Docker).

Ensure `.env` contains:
```
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000,http://localhost:5173,http://127.0.0.1:5173,http://localhost
```

### API Response Format

**Authentication endpoints return:**
```json
{
  "user": {
    "id": 1,
    "username": "testuser",
    "email": "test@example.com"
  },
  "tokens": {
    "access": "eyJhbGc...",
    "refresh": "eyJhbGc..."
  },
  "message": "User registered successfully"
}
```

**Validation rules:**
- Address fields: Minimum 1 character (allows abbreviations like "HKI", "TRE")
- Distance: Must be greater than 0
- Date: ISO format (YYYY-MM-DD)

### Testing with Frontend

1. Start backend: `python manage.py runserver`
2. Start frontend: `npm run dev` (in frontend directory)
3. Frontend available at: http://localhost:5173
4. Create user via register or use test credentials

## Security Features

- JWT token authentication with refresh
- Password hashing with Django's PBKDF2
- Input validation on all endpoints
- Rate limiting configured
- CORS properly configured
- SQL injection protection (Django ORM)
- XSS protection (Django defaults)
- CSRF protection for non-API endpoints
- Security headers (X-Frame-Options, X-Content-Type-Options, etc.)

## Testing

### Manual API Testing

See `TESTING_GUIDE.md` and `QUICK_REFERENCE.md` for comprehensive API testing examples with curl commands.

### Security Testing

Project has been tested with:
- npm audit (frontend dependencies): 0 vulnerabilities
- Nikto web scanner: No critical issues found
- Manual security review: Passed

## Deployment Notes

### Environment Variables for Production

Required:
- `SECRET_KEY` - Strong random string (use `python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'`)
- `DATABASE_URL` - PostgreSQL connection string
- `DEBUG` - Set to False
- `ALLOWED_HOSTS` - Your domain(s)
- `CORS_ALLOWED_ORIGINS` - Frontend URL(s)

Optional:
- `GOOGLE_MAPS_API_KEY` - For distance calculation
- `EMAIL_*` - For email notifications

### Database Migration
```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic
```

### Production Server

Use gunicorn or uwsgi instead of runserver:
```bash
gunicorn config.wsgi:application --bind 0.0.0.0:8000
```

## Project Status

**Completed:**
- User management API (registration, authentication, profile)
- Trip tracking API (CRUD operations, monthly summaries)
- Report generation API (PDF creation and download)
- JWT authentication with token refresh
- Input validation and security measures
- Docker containerization
- CI/CD pipeline with GitHub Actions
- Frontend integration tested and working
- Security audit completed (0 critical vulnerabilities)

**Future Enhancements:**
- Google Maps API integration for automatic distance calculation
- Celery for async PDF generation
- Email notifications for monthly reports
- Export to Excel format
- API rate limiting per user
- Comprehensive test suite
- API documentation with Swagger/OpenAPI
- Production deployment scripts

## License

Private project - CodeNob Dev

## Author

Sami - CodeNob Dev
- GitHub: https://github.com/Xmas178
- Backend: https://github.com/Xmas178/kilometri-tracker
- Frontend: https://github.com/Xmas178/kilometri-tracker-frontend
- Portfolio: www.tommilammi.fi