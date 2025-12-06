"""
URL routing for Trips app
Maps URL patterns to view functions

This file defines all URL endpoints for trip-related operations:
- Trip CRUD (Create, Read, Update, Delete)
- Distance calculation
- Monthly summaries
"""

from django.urls import path
from .views import (
    TripListCreateView,
    TripDetailView,
    CalculateDistanceView,
    MonthlySummaryView,
)

# App namespace for URL reversing
# Usage: reverse('trips:trip_list') returns '/api/trips/'
app_name = "trips"

urlpatterns = [
    # ========================================
    # Trip CRUD Endpoints
    # ========================================
    # GET /api/trips/
    # List all trips for authenticated user
    # Query params: ?search=..., ?ordering=..., ?date=..., ?is_manual=...
    # Returns: list of trips
    #
    # POST /api/trips/
    # Create new trip
    # Body: {"date": "...", "start_address": "...", "end_address": "...", "distance_km": ...}
    # Returns: created trip
    path("trips/", TripListCreateView.as_view(), name="trip_list"),
    # GET /api/trips/<id>/
    # View specific trip details
    # Returns: full trip data
    #
    # PUT/PATCH /api/trips/<id>/
    # Update specific trip
    # Body: {"date": "...", "start_address": "...", etc.}
    # Returns: updated trip
    #
    # DELETE /api/trips/<id>/
    # Delete specific trip
    # Returns: 204 No Content
    path("trips/<int:pk>/", TripDetailView.as_view(), name="trip_detail"),
    # ========================================
    # Google Maps Integration
    # ========================================
    # POST /api/trips/calculate-distance/
    # Calculate distance using Google Maps (without creating trip)
    # Body: {"start_address": "...", "end_address": "..."}
    # Returns: {"distance_km": ..., "duration_seconds": ..., "route_data": {...}}
    # Rate limit: 30 per minute per user
    path(
        "trips/calculate-distance/",
        CalculateDistanceView.as_view(),
        name="calculate_distance",
    ),
    # ========================================
    # Summary & Statistics
    # ========================================
    # GET /api/trips/monthly-summary/
    # Get monthly trip summary
    # Query params: ?year=2025&month=12
    # Returns: {"year": ..., "month": ..., "trip_count": ..., "total_km": ..., "trips": [...]}
    path(
        "trips/monthly-summary/", MonthlySummaryView.as_view(), name="monthly_summary"
    ),
]
