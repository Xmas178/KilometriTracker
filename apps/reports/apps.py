"""
Reports app configuration
Defines settings for the reports application
"""

from django.apps import AppConfig


class ReportsConfig(AppConfig):
    """
    Configuration class for Reports app

    Tells Django how to handle this application.
    The 'name' field MUST match the full Python path to the app.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.reports"  # CRITICAL: Full path including 'apps.'
    verbose_name = "Reports"  # Human-readable name in admin
