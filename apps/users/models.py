"""
User models for KilometriTracker
Extended Django User model with additional business-related fields

This file defines the custom User model that extends Django's AbstractUser.
We add company and phone fields for business trip tracking purposes.
"""

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Extended User model with company information

    Extends Django's built-in AbstractUser to add business-specific fields.

    Inherited fields from AbstractUser:
        - username: Unique username for login
        - email: User's email address
        - password: Hashed password (never stored in plain text)
        - first_name: User's first name
        - last_name: User's last name
        - is_active: Boolean - is account active?
        - is_staff: Boolean - can access admin panel?
        - is_superuser: Boolean - has all permissions?
        - date_joined: Timestamp when account was created
        - last_login: Timestamp of last login

    Additional fields:
        - company: Company name (optional)
        - phone: Contact phone number (optional)
        - created_at: Account creation timestamp
        - updated_at: Last profile update timestamp
    """

    # Company name - optional field for business users
    company = models.CharField(
        max_length=200,
        blank=True,  # Field is optional (can be empty)
        help_text="Company name (optional)",
    )

    # Contact phone number - optional field
    phone = models.CharField(
        max_length=20,
        blank=True,  # Field is optional
        help_text="Contact phone number (optional)",
    )

    # Timestamp when account was created
    # auto_now_add=True means Django sets this automatically on creation
    created_at = models.DateTimeField(
        auto_now_add=True, help_text="Account creation date"
    )

    # Timestamp when profile was last updated
    # auto_now=True means Django updates this automatically on every save
    updated_at = models.DateTimeField(
        auto_now=True, help_text="Last profile update date"
    )

    class Meta:
        """
        Model metadata

        Meta class defines model behavior and database settings
        """

        verbose_name = "User"  # Singular name in admin
        verbose_name_plural = "Users"  # Plural name in admin
        ordering = [
            "-created_at"
        ]  # Default ordering: newest first (- means descending)

    def __str__(self):
        """
        String representation of user

        This method defines how a User object appears as a string.
        Used in Django admin and when printing User objects.

        Returns:
            str: Username of the user
        """
        return self.username

    def get_full_name(self):
        """
        Return user's full name

        Combines first_name and last_name. If both are empty,
        returns username instead.

        Returns:
            str: Full name or username
        """
        full_name = f"{self.first_name} {self.last_name}".strip()
        return full_name or self.username
