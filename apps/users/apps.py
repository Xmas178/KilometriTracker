"""
Users app configuration
Defines settings for the users application
"""

from django.apps import AppConfig


class UsersConfig(AppConfig):
    """
    Configuration class for Users app

    Tells Django how to handle this application.
    The 'name' field MUST match the full Python path to the app.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.users"  # CRITICAL: Full path including 'apps.'
    verbose_name = "Users"  # Human-readable name in admin
