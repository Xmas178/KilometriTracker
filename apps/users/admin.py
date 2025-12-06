"""
Django admin configuration for Users app
Registers User model to admin panel with custom display
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """
    Custom admin interface for User model

    Extends Django's built-in UserAdmin to include our custom fields
    (company, phone) in the admin panel.
    """

    # Fields to display in user list view
    list_display = [
        "username",
        "email",
        "first_name",
        "last_name",
        "company",
        "is_staff",
        "created_at",
    ]

    # Fields to filter by in right sidebar
    list_filter = ["is_staff", "is_superuser", "is_active", "created_at"]

    # Fields to search by in search box
    search_fields = ["username", "email", "first_name", "last_name", "company"]

    # Add our custom fields to the user edit form
    # fieldsets defines how fields are grouped in the edit form
    fieldsets = BaseUserAdmin.fieldsets + (
        ("Additional Info", {"fields": ("company", "phone")}),
    )

    # Add our custom fields to the "Add User" form
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ("Additional Info", {"fields": ("company", "phone")}),
    )
