"""
Django admin configuration for Trips app
Registers Trip model to admin panel with custom display
"""

from django.contrib import admin
from .models import Trip


@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    """
    Custom admin interface for Trip model

    Provides a clean interface for viewing and managing trips
    in the Django admin panel.
    """

    # Fields to display in trip list view
    list_display = [
        "user",
        "date",
        "start_address",
        "end_address",
        "distance_km",
        "is_manual",
        "created_at",
    ]

    # Fields to filter by in right sidebar
    list_filter = ["is_manual", "date", "created_at", "user"]

    # Fields to search by in search box
    search_fields = ["start_address", "end_address", "purpose", "user__username"]

    # Default ordering in list view (newest first)
    ordering = ["-date", "-created_at"]

    # Read-only fields (can't be edited in admin)
    readonly_fields = ["created_at", "updated_at"]

    # How many trips to show per page
    list_per_page = 50

    # Date hierarchy navigation (year/month drill-down)
    date_hierarchy = "date"
