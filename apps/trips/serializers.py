"""
Trip serializers for KilometriTracker API
Convert Trip model to/from JSON for API responses and requests

This file contains serializers for:
- Trip creation (manual and Google Maps)
- Trip listing and detail views
- Trip updates
"""

from rest_framework import serializers
from .models import Trip
from apps.core.validators import validate_distance, validate_address, validate_trip_date


class TripSerializer(serializers.ModelSerializer):
    """
    Main serializer for Trip model

    Used for viewing and updating trips.
    Includes all trip fields plus computed fields.

    Read-only fields:
        - id: Trip database ID
        - user: Owner (set automatically from request.user)
        - created_at: Creation timestamp
        - updated_at: Last update timestamp
        - year_month: Computed (year, month) tuple
    """

    # Computed field: year and month as tuple
    # This is useful for grouping trips by month
    year_month = serializers.ReadOnlyField()

    # Display user as username instead of ID
    # This makes API responses more readable
    user_display = serializers.CharField(
        source="user.username", read_only=True, help_text="Username of trip owner"
    )

    class Meta:
        model = Trip
        fields = [
            "id",
            "user",
            "user_display",
            "date",
            "start_address",
            "end_address",
            "distance_km",
            "purpose",
            "is_manual",
            "route_data",
            "year_month",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "user",
            "user_display",
            "year_month",
            "created_at",
            "updated_at",
        ]

    def validate_date(self, value):
        """
        Validate trip date using custom validator

        Args:
            value (date): Trip date

        Returns:
            date: Validated date

        Raises:
            ValidationError: If date is invalid
        """
        validate_trip_date(value)
        return value

    def validate_start_address(self, value):
        """
        Validate start address using custom validator

        Args:
            value (str): Start address

        Returns:
            str: Validated address

        Raises:
            ValidationError: If address is invalid
        """
        validate_address(value)
        return value

    def validate_end_address(self, value):
        """
        Validate end address using custom validator

        Args:
            value (str): End address

        Returns:
            str: Validated address

        Raises:
            ValidationError: If address is invalid
        """
        validate_address(value)
        return value

    def validate_distance_km(self, value):
        """
        Validate distance using custom validator

        Args:
            value (Decimal): Distance in kilometers

        Returns:
            Decimal: Validated distance

        Raises:
            ValidationError: If distance is invalid
        """
        validate_distance(value)
        return value


class TripCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating new trips

    Used when creating trips (both manual and Google Maps).
    Does not include route_data in input (added by view if using Google Maps).

    Fields:
        - date: Trip date
        - start_address: Starting location
        - end_address: Destination
        - distance_km: Distance in kilometers
        - purpose: Optional trip description
        - is_manual: True if manually entered, False if Google Maps
    """

    class Meta:
        model = Trip
        fields = [
            "date",
            "start_address",
            "end_address",
            "distance_km",
            "purpose",
            "is_manual",
        ]

    def validate_date(self, value):
        """Validate trip date"""
        validate_trip_date(value)
        return value

    def validate_start_address(self, value):
        """Validate start address"""
        validate_address(value)
        return value

    def validate_end_address(self, value):
        """Validate end address"""
        validate_address(value)
        return value

    def validate_distance_km(self, value):
        """Validate distance"""
        validate_distance(value)
        return value

    def create(self, validated_data):
        """
        Create new trip

        Automatically sets user from request context.

        Args:
            validated_data (dict): Validated field values

        Returns:
            Trip: Created trip instance
        """
        # Get user from request context
        user = self.context["request"].user

        # Create trip with user
        trip = Trip.objects.create(user=user, **validated_data)

        return trip


class TripListSerializer(serializers.ModelSerializer):
    """
    Lightweight serializer for trip listings

    Used when listing multiple trips (performance optimization).
    Shows only essential information, excludes heavy fields like route_data.

    This is lighter than TripSerializer - faster for large lists.
    """

    # Display user as username
    user_display = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = Trip
        fields = [
            "id",
            "user_display",
            "date",
            "start_address",
            "end_address",
            "distance_km",
            "is_manual",
            "created_at",
        ]
        read_only_fields = ["id", "user_display", "created_at"]


class TripUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating existing trips

    Allows updating most fields except:
    - user (can't change trip owner)
    - is_manual (can't change entry type after creation)
    - route_data (Google Maps data is immutable)
    """

    class Meta:
        model = Trip
        fields = ["date", "start_address", "end_address", "distance_km", "purpose"]

    def validate_date(self, value):
        """Validate trip date"""
        validate_trip_date(value)
        return value

    def validate_start_address(self, value):
        """Validate start address"""
        validate_address(value)
        return value

    def validate_end_address(self, value):
        """Validate end address"""
        validate_address(value)
        return value

    def validate_distance_km(self, value):
        """Validate distance"""
        validate_distance(value)
        return value


class DistanceCalculationSerializer(serializers.Serializer):
    """
    Serializer for Google Maps distance calculation request

    Used when user wants to calculate distance automatically.
    This is NOT a Trip model serializer - it's for the calculation endpoint.

    Request body:
        {
            "start_address": "Oulu, Finland",
            "end_address": "Helsinki, Finland"
        }

    Response:
        {
            "distance_km": 607.5,
            "start_address": "Oulu, Finland",
            "end_address": "Helsinki, Finland",
            "route_data": {...}  # Google Maps API response
        }
    """

    start_address = serializers.CharField(
        max_length=500, help_text="Starting location address"
    )

    end_address = serializers.CharField(max_length=500, help_text="Destination address")

    def validate_start_address(self, value):
        """Validate start address"""
        validate_address(value)
        return value

    def validate_end_address(self, value):
        """Validate end address"""
        validate_address(value)
        return value
