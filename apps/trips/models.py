"""
Trip models for KilometriTracker
Business travel distance tracking with automatic and manual entry support

This file defines the Trip model which stores individual business trip entries.
Supports both Google Maps automatic calculation and manual distance entry.
"""

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings


class Trip(models.Model):
    """
    Individual business trip entry

    Represents a single business trip with starting point, destination,
    and distance traveled. Can be created either:
    1. Automatically - using Google Maps Distance Matrix API
    2. Manually - user enters addresses and distance themselves

    Fields:
        - user: Owner of this trip (ForeignKey to User)
        - date: When the trip took place
        - start_address: Starting location (text)
        - end_address: Destination location (text)
        - distance_km: Distance in kilometers (decimal)
        - purpose: Optional description/reason for trip
        - is_manual: True if manually entered, False if Google Maps calculated
        - route_data: JSON data from Google Maps (if available)
        - created_at: When this entry was created
        - updated_at: When this entry was last modified
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="trips",
        help_text="Trip owner",
    )

    date = models.DateField(help_text="Trip date")

    start_address = models.CharField(
        max_length=500, help_text="Starting location address"
    )

    end_address = models.CharField(max_length=500, help_text="Destination address")

    distance_km = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        validators=[
            MinValueValidator(0.01, message="Distance must be positive"),
            MaxValueValidator(9999.99, message="Distance seems unreasonably high"),
        ],
        help_text="Distance in kilometers",
    )

    purpose = models.CharField(
        max_length=500, blank=True, help_text="Trip purpose or description (optional)"
    )

    is_manual = models.BooleanField(
        default=False,
        help_text="True if distance was entered manually (not calculated)",
    )

    route_data = models.JSONField(
        null=True, blank=True, help_text="Google Maps API response data (if available)"
    )

    created_at = models.DateTimeField(
        auto_now_add=True, help_text="Entry creation timestamp"
    )

    updated_at = models.DateTimeField(auto_now=True, help_text="Last update timestamp")

    class Meta:
        verbose_name = "Trip"
        verbose_name_plural = "Trips"
        ordering = ["-date", "-created_at"]
        indexes = [
            models.Index(fields=["user", "date"]),
            models.Index(fields=["date"]),
            models.Index(fields=["user", "-created_at"]),
        ]

    def __str__(self):
        return f"{self.start_address} → {self.end_address} ({self.distance_km} km)"

    @property
    def year_month(self):
        return (self.date.year, self.date.month)
