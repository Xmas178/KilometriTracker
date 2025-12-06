"""
Trips app configuration
Defines settings for the trips application
"""

from django.apps import AppConfig


class TripsConfig(AppConfig):
    """
    Configuration class for Trips app

    Tells Django how to handle this application.
    The 'name' field MUST match the full Python path to the app.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.trips"  # CRITICAL: Full path including 'apps.'
    verbose_name = "Trips"  # Human-readable name in admin
