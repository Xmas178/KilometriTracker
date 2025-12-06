"""
Django admin configuration for Reports app
Registers MonthlyReport model to admin panel with custom display
"""

from django.contrib import admin
from .models import MonthlyReport


@admin.register(MonthlyReport)
class MonthlyReportAdmin(admin.ModelAdmin):
    """
    Custom admin interface for MonthlyReport model

    Provides a clean interface for viewing and managing monthly reports
    in the Django admin panel.
    """

    # Fields to display in report list view
    list_display = [
        "user",
        "period_display",
        "total_km",
        "trip_count",
        "sent_at",
        "created_at",
    ]

    # Fields to filter by in right sidebar
    list_filter = ["year", "month", "sent_at", "created_at", "user"]

    # Fields to search by in search box
    search_fields = ["user__username", "user__email"]

    # Default ordering (newest first)
    ordering = ["-year", "-month"]

    # Read-only fields (can't be edited in admin)
    readonly_fields = ["created_at"]

    # How many reports to show per page
    list_per_page = 50
