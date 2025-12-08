# KilometriTracker API - Quick Reference

Quick copy-paste curl commands for testing. No explanations, just commands.

---

## Setup
```bash
# Start server
cd /home/crake178/projects/kilometri-tracker/backend
source venv/bin/activate
python manage.py runserver
```

---

## Authentication

### Register
```bash
curl -X POST http://127.0.0.1:8000/api/auth/register/ -H "Content-Type: application/json" -d '{"username": "testuser", "email": "test@example.com", "password": "salasana123", "password2": "salasana123", "first_name": "Test", "last_name": "User", "company": "TestCorp"}'
```

### Login & Save Token
```bash
curl -X POST http://127.0.0.1:8000/api/auth/login/ -H "Content-Type: application/json" -d '{"username": "testuser", "password": "salasana123"}'

# Save token (replace with your actual token)
TOKEN="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

### View Profile
```bash
curl -X GET http://127.0.0.1:8000/api/auth/profile/ -H "Authorization: Bearer $TOKEN"
```

### Update Profile
```bash
curl -X PATCH http://127.0.0.1:8000/api/auth/profile/ -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" -d '{"first_name": "Updated", "company": "NewCompany"}'
```

### Change Password
```bash
curl -X POST http://127.0.0.1:8000/api/auth/change-password/ -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" -d '{"old_password": "salasana123", "new_password": "uusisalasana456", "new_password2": "uusisalasana456"}'
```

### Logout
```bash
curl -X POST http://127.0.0.1:8000/api/auth/logout/ -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" -d '{"refresh": "YOUR_REFRESH_TOKEN"}'
```

---

## Trips

### Create Trip (Manual)
```bash
curl -X POST http://127.0.0.1:8000/api/trips/ -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" -d '{"date": "2025-12-08", "start_address": "Oulu, Finland", "end_address": "Helsinki, Finland", "distance_km": 607.5, "purpose": "Business meeting", "is_manual": true}'
```

### List Trips
```bash
curl -X GET http://127.0.0.1:8000/api/trips/ -H "Authorization: Bearer $TOKEN"
```

### Get Trip Details
```bash
curl -X GET http://127.0.0.1:8000/api/trips/1/ -H "Authorization: Bearer $TOKEN"
```

### Update Trip
```bash
curl -X PATCH http://127.0.0.1:8000/api/trips/1/ -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" -d '{"distance_km": 610.0, "purpose": "Updated purpose"}'
```

### Delete Trip
```bash
curl -X DELETE http://127.0.0.1:8000/api/trips/1/ -H "Authorization: Bearer $TOKEN"
```

### Calculate Distance (Google Maps)
```bash
curl -X POST http://127.0.0.1:8000/api/trips/calculate-distance/ -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" -d '{"start_address": "Oulu, Finland", "end_address": "Helsinki, Finland"}'
```

### Monthly Summary
```bash
curl -X GET "http://127.0.0.1:8000/api/trips/monthly-summary/?year=2025&month=12" -H "Authorization: Bearer $TOKEN"
```

---

## Reports

### Generate Report
```bash
curl -X POST http://127.0.0.1:8000/api/reports/generate/ -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" -d '{"year": 2025, "month": 12}'
```

### List Reports
```bash
curl -X GET http://127.0.0.1:8000/api/reports/ -H "Authorization: Bearer $TOKEN"
```

### Get Report Details
```bash
curl -X GET http://127.0.0.1:8000/api/reports/1/ -H "Authorization: Bearer $TOKEN"
```

---

## Filtering & Search

### Filter by Date
```bash
curl -X GET "http://127.0.0.1:8000/api/trips/?date=2025-12-08" -H "Authorization: Bearer $TOKEN"
```

### Filter by Type
```bash
curl -X GET "http://127.0.0.1:8000/api/trips/?is_manual=true" -H "Authorization: Bearer $TOKEN"
```

### Search
```bash
curl -X GET "http://127.0.0.1:8000/api/trips/?search=Helsinki" -H "Authorization: Bearer $TOKEN"
```

### Ordering
```bash
# By distance (descending)
curl -X GET "http://127.0.0.1:8000/api/trips/?ordering=-distance_km" -H "Authorization: Bearer $TOKEN"

# By date (ascending)
curl -X GET "http://127.0.0.1:8000/api/trips/?ordering=date" -H "Authorization: Bearer $TOKEN"
```

### Pagination
```bash
curl -X GET "http://127.0.0.1:8000/api/trips/?page=2" -H "Authorization: Bearer $TOKEN"
```

---

## Admin Credentials

- **URL:** http://127.0.0.1:8000/admin/
- **Username:** admin
- **Password:** salasana1234

---

## Pretty JSON Output
```bash
# Install jq
sudo apt-get install jq

# Use with curl
curl -X GET http://127.0.0.1:8000/api/trips/ -H "Authorization: Bearer $TOKEN" | jq
```

---

## Rate Limits

- Register: 3/hour per IP
- Change Password: 3/15min per user
- Logout: 10/min per user
- Calculate Distance: 30/min per user