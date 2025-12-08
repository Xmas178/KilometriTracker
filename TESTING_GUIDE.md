# KilometriTracker API - Testing Guide

Complete guide for testing all API endpoints with curl commands and expected responses.

---

## Prerequisites

**Backend must be running:**
```bash
cd /home/crake178/projects/kilometri-tracker/backend
source venv/bin/activate
python manage.py runserver
```

**Server runs at:** `http://127.0.0.1:8000/`

---

## Authentication Flow

All endpoints (except registration and login) require JWT authentication.

### 1. Register New User

**Endpoint:** `POST /api/auth/register/`
```bash
curl -X POST http://127.0.0.1:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "salasana123",
    "password2": "salasana123",
    "first_name": "Test",
    "last_name": "User",
    "company": "TestCorp",
    "phone": "+358 123 456789"
  }'
```

**Expected Response (201 Created):**
```json
{
  "user": {
    "id": 1,
    "username": "testuser",
    "email": "test@example.com",
    "first_name": "Test",
    "last_name": "User",
    "company": "TestCorp",
    "phone": "+358 123 456789",
    "created_at": "2025-12-08T16:00:00+02:00",
    "updated_at": "2025-12-08T16:00:00+02:00"
  },
  "tokens": {
    "refresh": "eyJhbGciOiJIUzI1NiIs...",
    "access": "eyJhbGciOiJIUzI1NiIs..."
  },
  "message": "User registered successfully"
}
```

**Save the access token!** You'll need it for authenticated requests.

---

### 2. Login (Get JWT Tokens)

**Endpoint:** `POST /api/auth/login/`
```bash
curl -X POST http://127.0.0.1:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "salasana123"
  }'
```

**Expected Response (200 OK):**
```json
{
  "refresh": "eyJhbGciOiJIUzI1NiIs...",
  "access": "eyJhbGciOiJIUzI1NiIs..."
}
```

**Save access token to environment variable:**
```bash
TOKEN="<paste_your_access_token_here>"
```

Or extract automatically (Linux/Mac):
```bash
TOKEN=$(curl -s -X POST http://127.0.0.1:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "password": "salasana123"}' \
  | grep -o '"access":"[^"]*' | cut -d'"' -f4)

echo "Token saved: $TOKEN"
```

---

### 3. View User Profile

**Endpoint:** `GET /api/auth/profile/`
```bash
curl -X GET http://127.0.0.1:8000/api/auth/profile/ \
  -H "Authorization: Bearer $TOKEN"
```

**Expected Response (200 OK):**
```json
{
  "id": 1,
  "username": "testuser",
  "email": "test@example.com",
  "first_name": "Test",
  "last_name": "User",
  "company": "TestCorp",
  "phone": "+358 123 456789",
  "created_at": "2025-12-08T16:00:00+02:00",
  "updated_at": "2025-12-08T16:00:00+02:00"
}
```

---

### 4. Update User Profile

**Endpoint:** `PUT /api/auth/profile/` or `PATCH /api/auth/profile/`
```bash
curl -X PATCH http://127.0.0.1:8000/api/auth/profile/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Updated",
    "company": "NewCompany"
  }'
```

**Expected Response (200 OK):**
```json
{
  "id": 1,
  "username": "testuser",
  "email": "test@example.com",
  "first_name": "Updated",
  "last_name": "User",
  "company": "NewCompany",
  ...
}
```

---

### 5. Change Password

**Endpoint:** `POST /api/auth/change-password/`
```bash
curl -X POST http://127.0.0.1:8000/api/auth/change-password/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "old_password": "salasana123",
    "new_password": "uusisalasana456",
    "new_password2": "uusisalasana456"
  }'
```

**Expected Response (200 OK):**
```json
{
  "message": "Password changed successfully"
}
```

---

### 6. Logout

**Endpoint:** `POST /api/auth/logout/`
```bash
curl -X POST http://127.0.0.1:8000/api/auth/logout/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "refresh": "<your_refresh_token>"
  }'
```

**Expected Response (200 OK):**
```json
{
  "message": "Logged out successfully"
}
```

---

## Trip Management

### 1. Create Trip (Manual Entry)

**Endpoint:** `POST /api/trips/`
```bash
curl -X POST http://127.0.0.1:8000/api/trips/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "date": "2025-12-08",
    "start_address": "Oulu, Finland",
    "end_address": "Helsinki, Finland",
    "distance_km": 607.5,
    "purpose": "Business meeting",
    "is_manual": true
  }'
```

**Expected Response (201 Created):**
```json
{
  "date": "2025-12-08",
  "start_address": "Oulu, Finland",
  "end_address": "Helsinki, Finland",
  "distance_km": "607.50",
  "purpose": "Business meeting",
  "is_manual": true
}
```

---

### 2. List All Trips

**Endpoint:** `GET /api/trips/`
```bash
curl -X GET http://127.0.0.1:8000/api/trips/ \
  -H "Authorization: Bearer $TOKEN"
```

**Expected Response (200 OK):**
```json
{
  "count": 1,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "user_display": "testuser",
      "date": "2025-12-08",
      "start_address": "Oulu, Finland",
      "end_address": "Helsinki, Finland",
      "distance_km": "607.50",
      "is_manual": true,
      "created_at": "2025-12-08T16:00:00+02:00"
    }
  ]
}
```

---

### 3. Get Trip Details

**Endpoint:** `GET /api/trips/<id>/`
```bash
curl -X GET http://127.0.0.1:8000/api/trips/1/ \
  -H "Authorization: Bearer $TOKEN"
```

**Expected Response (200 OK):**
```json
{
  "id": 1,
  "user": 1,
  "user_display": "testuser",
  "date": "2025-12-08",
  "start_address": "Oulu, Finland",
  "end_address": "Helsinki, Finland",
  "distance_km": "607.50",
  "purpose": "Business meeting",
  "is_manual": true,
  "route_data": null,
  "year_month": [2025, 12],
  "created_at": "2025-12-08T16:00:00+02:00",
  "updated_at": "2025-12-08T16:00:00+02:00"
}
```

---

### 4. Update Trip

**Endpoint:** `PUT /api/trips/<id>/` or `PATCH /api/trips/<id>/`
```bash
curl -X PATCH http://127.0.0.1:8000/api/trips/1/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "distance_km": 610.0,
    "purpose": "Updated purpose"
  }'
```

**Expected Response (200 OK):**
```json
{
  "date": "2025-12-08",
  "start_address": "Oulu, Finland",
  "end_address": "Helsinki, Finland",
  "distance_km": "610.00",
  "purpose": "Updated purpose"
}
```

---

### 5. Delete Trip

**Endpoint:** `DELETE /api/trips/<id>/`
```bash
curl -X DELETE http://127.0.0.1:8000/api/trips/1/ \
  -H "Authorization: Bearer $TOKEN"
```

**Expected Response (204 No Content):**
No response body.

---

### 6. Calculate Distance (Google Maps)

**Endpoint:** `POST /api/trips/calculate-distance/`

**⚠️ Note:** Requires Google Maps API key configured in `.env`
```bash
curl -X POST http://127.0.0.1:8000/api/trips/calculate-distance/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "start_address": "Oulu, Finland",
    "end_address": "Helsinki, Finland"
  }'
```

**Expected Response (200 OK):**
```json
{
  "distance_km": 607.5,
  "distance_meters": 607500,
  "duration_seconds": 21600,
  "start_address": "Oulu, Finland",
  "end_address": "Helsinki, Finland",
  "route_data": {
    "rows": [...],
    "origin_addresses": ["Oulu, Finland"],
    "destination_addresses": ["Helsinki, Finland"]
  }
}
```

**Without API key:**
```json
{
  "error": "Google Maps API is not configured. Please add GOOGLE_MAPS_API_KEY to environment variables."
}
```

---

### 7. Monthly Trip Summary

**Endpoint:** `GET /api/trips/monthly-summary/`
```bash
curl -X GET "http://127.0.0.1:8000/api/trips/monthly-summary/?year=2025&month=12" \
  -H "Authorization: Bearer $TOKEN"
```

**Query Parameters:**
- `year` (optional): Year (defaults to current year)
- `month` (optional): Month 1-12 (defaults to current month)

**Expected Response (200 OK):**
```json
{
  "year": 2025,
  "month": 12,
  "trip_count": 1,
  "total_km": 607.5,
  "manual_count": 1,
  "automatic_count": 0,
  "trips": [
    {
      "id": 1,
      "user_display": "testuser",
      "date": "2025-12-08",
      "start_address": "Oulu, Finland",
      "end_address": "Helsinki, Finland",
      "distance_km": "607.50",
      "is_manual": true,
      "created_at": "2025-12-08T16:00:00+02:00"
    }
  ]
}
```

---

## Monthly Reports

### 1. Generate Monthly Report

**Endpoint:** `POST /api/reports/generate/`
```bash
curl -X POST http://127.0.0.1:8000/api/reports/generate/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "year": 2025,
    "month": 12
  }'
```

**Expected Response (201 Created):**
```json
{
  "id": 1,
  "user": 1,
  "user_display": "testuser",
  "year": 2025,
  "month": 12,
  "period_display": "December 2025",
  "total_km": "607.50",
  "trip_count": 1,
  "pdf_file": null,
  "pdf_url": null,
  "excel_file": null,
  "excel_url": null,
  "sent_at": null,
  "created_at": "2025-12-08T16:00:00+02:00"
}
```

**If report already exists (409 Conflict):**
```json
{
  "error": "Report for 2025/12 already exists",
  "report": {
    "id": 1,
    ...
  }
}
```

**If no trips found (400 Bad Request):**
```json
{
  "error": "No trips found for 2025/12. Cannot generate empty report."
}
```

---

### 2. List All Reports

**Endpoint:** `GET /api/reports/`
```bash
curl -X GET http://127.0.0.1:8000/api/reports/ \
  -H "Authorization: Bearer $TOKEN"
```

**Expected Response (200 OK):**
```json
{
  "count": 1,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "user": 1,
      "user_display": "testuser",
      "year": 2025,
      "month": 12,
      "period_display": "December 2025",
      "total_km": "607.50",
      "trip_count": 1,
      "pdf_file": null,
      "pdf_url": null,
      "excel_file": null,
      "excel_url": null,
      "sent_at": null,
      "created_at": "2025-12-08T16:00:00+02:00"
    }
  ]
}
```

---

### 3. Get Report Details

**Endpoint:** `GET /api/reports/<id>/`
```bash
curl -X GET http://127.0.0.1:8000/api/reports/1/ \
  -H "Authorization: Bearer $TOKEN"
```

**Expected Response (200 OK):**
```json
{
  "id": 1,
  "user": 1,
  "user_display": "testuser",
  "year": 2025,
  "month": 12,
  "period_display": "December 2025",
  "total_km": "607.50",
  "trip_count": 1,
  "pdf_file": null,
  "pdf_url": null,
  "excel_file": null,
  "excel_url": null,
  "sent_at": null,
  "created_at": "2025-12-08T16:00:00+02:00"
}
```

---

## Admin Panel Testing

### Access Admin Panel

1. Navigate to: `http://127.0.0.1:8000/admin/`
2. Login with superuser credentials:
   - Username: `admin`
   - Password: `salasana1234`

### Available Admin Sections

- **Users** - Manage user accounts
- **Trips** - View/edit/delete trips
- **Monthly Reports** - View/edit reports
- **Groups** - User groups (Django built-in)
- **Periodic Tasks** - Celery tasks (future feature)

---

## Error Responses

### 400 Bad Request
```json
{
  "field_name": ["Error message"]
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
  "detail": "You do not have permission to perform this action."
}
```

### 404 Not Found
```json
{
  "detail": "Not found."
}
```

### 429 Too Many Requests (Rate Limiting)
```json
{
  "detail": "Request was throttled."
}
```

### 500 Internal Server Error
```json
{
  "error": "An unexpected error occurred"
}
```

---

## Rate Limits

| Endpoint | Limit | Key |
|----------|-------|-----|
| `/api/auth/register/` | 3 per hour | IP address |
| `/api/auth/change-password/` | 3 per 15 min | User |
| `/api/auth/logout/` | 10 per minute | User |
| `/api/trips/calculate-distance/` | 30 per minute | User |

---

## Testing Tips

### 1. Use jq for Pretty JSON Output
```bash
# Install jq (if not installed)
sudo apt-get install jq

# Use with curl
curl -X GET http://127.0.0.1:8000/api/trips/ \
  -H "Authorization: Bearer $TOKEN" | jq
```

### 2. Save Token to File
```bash
# Save token
echo $TOKEN > token.txt

# Load token
TOKEN=$(cat token.txt)
```

### 3. Test Pagination
```bash
# Get page 2
curl -X GET "http://127.0.0.1:8000/api/trips/?page=2" \
  -H "Authorization: Bearer $TOKEN"
```

### 4. Test Filtering
```bash
# Filter by date
curl -X GET "http://127.0.0.1:8000/api/trips/?date=2025-12-08" \
  -H "Authorization: Bearer $TOKEN"

# Filter by is_manual
curl -X GET "http://127.0.0.1:8000/api/trips/?is_manual=true" \
  -H "Authorization: Bearer $TOKEN"
```

### 5. Test Search
```bash
# Search in addresses and purpose
curl -X GET "http://127.0.0.1:8000/api/trips/?search=Helsinki" \
  -H "Authorization: Bearer $TOKEN"
```

### 6. Test Ordering
```bash
# Order by distance (descending)
curl -X GET "http://127.0.0.1:8000/api/trips/?ordering=-distance_km" \
  -H "Authorization: Bearer $TOKEN"
```

---

## Troubleshooting

### Token Expired

**Symptom:**
```json
{
  "detail": "Token is invalid or expired",
  "code": "token_not_valid"
}
```

**Solution:** Login again to get new token.

### CORS Errors (Browser)

**Symptom:** Browser console shows CORS error.

**Solution:** Check `CORS_ALLOWED_ORIGINS` in `.env` includes your frontend URL.

### Rate Limit Hit

**Symptom:**
```json
{
  "detail": "Request was throttled."
}
```

**Solution:** Wait for rate limit window to expire, or test with different user/IP.

---

## Next Steps

After testing all endpoints:

1. ✅ All tests passing? **Proceed to deployment**
2. ❌ Found bugs? **Check Django logs** (`python manage.py runserver` output)
3. 📝 Need more endpoints? **Refer to project roadmap in README.md**

---

**Happy Testing! **