"""
Trip views for KilometriTracker API
Handle trip CRUD operations and distance calculation

This file contains API endpoints for:
- Trip creation (manual and automatic)
- Trip listing and filtering
- Trip detail/update/delete
- Distance calculation using Google Maps
- Monthly trip summary
"""

from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.utils.decorators import method_decorator
from django_ratelimit.decorators import ratelimit
from datetime import date
from decimal import Decimal

from .models import Trip
from .serializers import (
    TripSerializer,
    TripCreateSerializer,
    TripListSerializer,
    TripUpdateSerializer,
    DistanceCalculationSerializer,
)
from .services import GoogleMapsService
from apps.core.permissions import IsOwner
from apps.core.exceptions import GoogleMapsAPIError, InvalidAddressError
import logging

logger = logging.getLogger(__name__)


class TripListCreateView(generics.ListCreateAPIView):
    """
    API endpoint for listing and creating trips

    GET /api/trips/
    List all trips for the authenticated user

    POST /api/trips/
    Create new trip (manual or with Google Maps)

    Query parameters (GET):
        - search: Search in addresses and purpose
        - ordering: Sort by field (e.g., -date for newest first)
        - date: Filter by exact date
        - is_manual: Filter by entry type (true/false)
        - date_after: Filter trips after this date
        - date_before: Filter trips before this date

    Request body (POST):
        {
            "date": "2025-12-06",
            "start_address": "Oulu, Finland",
            "end_address": "Helsinki, Finland",
            "distance_km": 607.5,
            "purpose": "Business meeting",
            "is_manual": true
        }

    Response (200 OK for GET, 201 Created for POST):
        [
            {
                "id": 1,
                "user_display": "sami",
                "date": "2025-12-06",
                "start_address": "Oulu, Finland",
                "end_address": "Helsinki, Finland",
                "distance_km": "607.50",
                "purpose": "Business meeting",
                "is_manual": false,
                "route_data": {...},
                "year_month": [2025, 12],
                "created_at": "2025-12-06T20:00:00Z",
                "updated_at": "2025-12-06T20:00:00Z"
            }
        ]
    """

    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    # Filtering options
    filterset_fields = ["date", "is_manual"]

    # Search in these fields
    search_fields = ["start_address", "end_address", "purpose"]

    # Allow ordering by these fields
    ordering_fields = ["date", "distance_km", "created_at"]
    ordering = ["-date", "-created_at"]  # Default: newest first

    def get_queryset(self):
        """
        Return trips for the current user only

        Users can only see their own trips.
        Supports additional filtering by date range.

        Returns:
            QuerySet: Filtered trips
        """
        # Base queryset: only current user's trips
        queryset = Trip.objects.filter(user=self.request.user)

        # Additional date range filtering
        date_after = self.request.query_params.get("date_after", None)
        date_before = self.request.query_params.get("date_before", None)

        if date_after:
            queryset = queryset.filter(date__gte=date_after)

        if date_before:
            queryset = queryset.filter(date__lte=date_before)

        return queryset

    def get_serializer_class(self):
        """
        Return appropriate serializer based on action

        - GET: Use lightweight TripListSerializer
        - POST: Use TripCreateSerializer

        Returns:
            Serializer class
        """
        if self.request.method == "POST":
            return TripCreateSerializer
        return TripListSerializer


class TripDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint for viewing, updating, and deleting a specific trip

    GET /api/trips/<id>/
    Retrieve trip details

    PUT/PATCH /api/trips/<id>/
    Update trip (partial or full update)

    DELETE /api/trips/<id>/
    Delete trip

    Permissions:
        - User must be authenticated
        - User must own the trip

    Request body (PUT/PATCH):
        {
            "date": "2025-12-06",
            "start_address": "Updated address",
            "end_address": "Updated destination",
            "distance_km": 650.0,
            "purpose": "Updated purpose"
        }
    """

    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        """
        Return trips for the current user only

        IsOwner permission will ensure user can only access their own trips.

        Returns:
            QuerySet: User's trips
        """
        return Trip.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        """
        Return appropriate serializer based on action

        - GET: Full TripSerializer with all fields
        - PUT/PATCH: TripUpdateSerializer (limited fields)
        - DELETE: No serializer needed

        Returns:
            Serializer class
        """
        if self.request.method in ["PUT", "PATCH"]:
            return TripUpdateSerializer
        return TripSerializer


@method_decorator(ratelimit(key="user", rate="30/m", method="POST"), name="dispatch")
class CalculateDistanceView(APIView):
    """
    API endpoint for calculating distance using Google Maps

    POST /api/trips/calculate-distance/

    Rate limit: 30 requests per minute per user
    This prevents excessive API costs.

    Calculate distance between two addresses without creating a trip.
    Useful for:
    - Previewing distance before creating trip
    - Validating addresses
    - Getting route information

    Request body:
        {
            "start_address": "Oulu, Finland",
            "end_address": "Helsinki, Finland"
        }

    Response (200 OK):
        {
            "distance_km": 607.5,
            "distance_meters": 607500,
            "duration_seconds": 21600,
            "start_address": "Oulu, Finland",  # Geocoded by Google
            "end_address": "Helsinki, Finland",  # Geocoded by Google
            "route_data": {...}  # Full Google Maps response
        }

    Error responses:
        400 Bad Request: Invalid addresses
        503 Service Unavailable: Google Maps API error
    """

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        """
        Handle POST request - calculate distance

        Args:
            request: HTTP request object

        Returns:
            Response: Distance data or error message
        """
        # Validate request data
        serializer = DistanceCalculationSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        start_address = serializer.validated_data["start_address"]
        end_address = serializer.validated_data["end_address"]

        try:
            # Initialize Google Maps service
            maps_service = GoogleMapsService()

            # Calculate distance
            result = maps_service.calculate_distance(start_address, end_address)

            logger.info(
                f"Distance calculated for user {request.user.username}: "
                f"{result['distance_km']} km"
            )

            return Response(result, status=status.HTTP_200_OK)

        except InvalidAddressError as e:
            # Address validation failed
            logger.warning(f"Invalid address: {str(e)}")
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        except GoogleMapsAPIError as e:
            # Google Maps API error
            logger.error(f"Google Maps API error: {str(e)}")
            return Response(
                {"error": str(e)}, status=status.HTTP_503_SERVICE_UNAVAILABLE
            )

        except Exception as e:
            # Unexpected error
            logger.exception(f"Unexpected error in calculate_distance: {str(e)}")
            return Response(
                {"error": "An unexpected error occurred"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class MonthlySummaryView(APIView):
    """
    API endpoint for monthly trip summary

    GET /api/trips/monthly-summary/

    Get summary of trips for a specific month.
    If no month specified, returns current month.

    Query parameters:
        - year: Year (e.g., 2025)
        - month: Month (1-12)

    Response (200 OK):
        {
            "year": 2025,
            "month": 12,
            "trip_count": 15,
            "total_km": 3250.50,
            "manual_count": 5,
            "automatic_count": 10,
            "trips": [...]  # List of trips for this month
        }

    Example:
        GET /api/trips/monthly-summary/?year=2025&month=12
    """

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """
        Handle GET request - return monthly summary

        Args:
            request: HTTP request object

        Returns:
            Response: Monthly summary data
        """
        # Get year and month from query params
        # Default to current month if not specified
        today = date.today()
        year = int(request.query_params.get("year", today.year))
        month = int(request.query_params.get("month", today.month))

        # Validate month
        if not 1 <= month <= 12:
            return Response(
                {"error": "Month must be between 1 and 12"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Get user's trips for this month
        trips = Trip.objects.filter(
            user=request.user, date__year=year, date__month=month
        ).order_by("-date")

        # Calculate summary statistics
        trip_count = trips.count()
        total_km = (
            sum(trip.distance_km for trip in trips)
            if trip_count > 0
            else Decimal("0.00")
        )
        manual_count = trips.filter(is_manual=True).count()
        automatic_count = trips.filter(is_manual=False).count()

        # Serialize trips
        trip_serializer = TripListSerializer(trips, many=True)

        # Prepare response
        summary = {
            "year": year,
            "month": month,
            "trip_count": trip_count,
            "total_km": total_km,
            "manual_count": manual_count,
            "automatic_count": automatic_count,
            "trips": trip_serializer.data,
        }

        logger.info(
            f"Monthly summary for {request.user.username}: "
            f"{year}/{month} - {trip_count} trips, {total_km} km"
        )

        return Response(summary, status=status.HTTP_200_OK)
