"""
Main URL configuration for KilometriTracker
Routes requests to appropriate app URLs

This is the root URL configuration. All URLs start here and
are then distributed to app-specific URL files.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # ========================================
    # Django Admin
    # ========================================
    # Django admin panel
    # http://127.0.0.1:8000/admin/
    path("admin/", admin.site.urls),
    # ========================================
    # API Endpoints
    # ========================================
    # All API endpoints are prefixed with /api/
    # User/Auth API endpoints
    # Examples:
    #   - http://127.0.0.1:8000/api/auth/register/
    #   - http://127.0.0.1:8000/api/auth/login/
    #   - http://127.0.0.1:8000/api/users/
    path("api/", include("apps.users.urls")),
    # Trip API endpoints
    # Examples:
    #   - http://127.0.0.1:8000/api/trips/
    #   - http://127.0.0.1:8000/api/trips/calculate-distance/
    path("api/", include("apps.trips.urls")),
    # Report API endpoints
    # Examples:
    #   - http://127.0.0.1:8000/api/reports/
    #   - http://127.0.0.1:8000/api/reports/generate/
    path("api/", include("apps.reports.urls")),
]

# Serve media files in development
# In production, use nginx or similar
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
