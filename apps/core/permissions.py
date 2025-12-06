"""
Custom permissions for KilometriTracker API
Define who can access and modify what data

This file contains permission classes that control access to API endpoints.
Django REST Framework checks these permissions before allowing operations.

Permission hierarchy:
1. IsAuthenticated - user must be logged in
2. IsOwner - user can only access their own data
3. IsAdminOrReadOnly - admins can modify, others can only read
"""

from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """
    Permission class: Only the owner can access/modify the object

    This permission ensures users can only access their own data.
    For example:
    - User A can only see/edit/delete their own trips
    - User B cannot access User A's trips

    Usage in views:
        permission_classes = [IsAuthenticated, IsOwner]

    How it works:
    - Checks if object.user == request.user
    - Returns True if match, False otherwise
    """

    def has_object_permission(self, request, view, obj):
        """
        Check if user owns this object

        Args:
            request: HTTP request object (contains user info)
            view: API view that's being accessed
            obj: Database object being accessed (Trip, MonthlyReport, etc.)

        Returns:
            bool: True if user owns the object, False otherwise

        Example:
            trip = Trip.objects.get(id=5)  # trip.user = User A
            request.user = User B

            has_object_permission(request, view, trip)  # Returns False
        """

        # Check if object has a 'user' field
        # All our models (Trip, MonthlyReport) have user field
        if not hasattr(obj, "user"):
            # If object doesn't have user field, deny access
            # This is a safety check
            return False

        # Compare object's user with request's user
        # Returns True only if they match
        return obj.user == request.user


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Permission class: Owner can modify, others can only read

    This permission allows:
    - Owner: Full access (GET, POST, PUT, PATCH, DELETE)
    - Others: Read-only access (GET only)

    Usage example:
        Public trip sharing feature (future):
        - Trip owner can edit/delete their trip
        - Other users can view the trip but not modify it

    NOTE: Not currently used in MVP, but useful for future features
    """

    def has_object_permission(self, request, view, obj):
        """
        Check permissions based on request method

        Safe methods (GET, HEAD, OPTIONS) are allowed for everyone.
        Unsafe methods (POST, PUT, PATCH, DELETE) only for owner.

        Args:
            request: HTTP request object
            view: API view being accessed
            obj: Database object being accessed

        Returns:
            bool: True if allowed, False otherwise
        """

        # SAFE_METHODS = ('GET', 'HEAD', 'OPTIONS')
        # These methods don't modify data, so anyone can use them
        if request.method in permissions.SAFE_METHODS:
            return True

        # For unsafe methods (POST, PUT, DELETE), check ownership
        if not hasattr(obj, "user"):
            return False

        return obj.user == request.user


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Permission class: Admins can modify, regular users can only read

    This permission allows:
    - Admin users (is_staff=True): Full access
    - Regular users: Read-only access

    Usage example:
        System-wide settings or statistics endpoints:
        - Admins can modify settings
        - Users can view statistics but not modify them

    NOTE: Not currently used in MVP, but useful for admin features
    """

    def has_permission(self, request, view):
        """
        Check permissions at view level (before accessing specific object)

        Args:
            request: HTTP request object
            view: API view being accessed

        Returns:
            bool: True if allowed, False otherwise
        """

        # Allow safe methods for everyone
        if request.method in permissions.SAFE_METHODS:
            return True

        # For unsafe methods, check if user is staff/admin
        return request.user and request.user.is_staff


class IsAuthenticatedOrCreateOnly(permissions.BasePermission):
    """
    Permission class: Anyone can create, but must be authenticated for other actions

    This permission allows:
    - Unauthenticated users: Can only POST (create/register)
    - Authenticated users: Full access

    Usage example:
        User registration endpoint:
        - Unauthenticated users can POST to create account
        - Must be logged in to view/edit profile

    This is specifically useful for the registration endpoint.
    """

    def has_permission(self, request, view):
        """
        Check permissions at view level

        Args:
            request: HTTP request object
            view: API view being accessed

        Returns:
            bool: True if allowed, False otherwise
        """

        # Allow POST for everyone (registration)
        if request.method == "POST":
            return True

        # For other methods, require authentication
        return request.user and request.user.is_authenticated


class IsSelfOrAdmin(permissions.BasePermission):
    """
    Permission class: Users can access their own data, admins can access everything

    This permission allows:
    - Regular user: Can only access their own user object
    - Admin user: Can access any user object

    Usage example:
        User profile endpoints:
        - User can view/edit their own profile
        - Admin can view/edit any user's profile
    """

    def has_object_permission(self, request, view, obj):
        """
        Check if user is accessing their own object or is admin

        Args:
            request: HTTP request object
            view: API view being accessed
            obj: User object being accessed

        Returns:
            bool: True if allowed, False otherwise
        """

        # Admin users can access everything
        if request.user and request.user.is_staff:
            return True

        # Regular users can only access their own user object
        # obj is the User object being accessed
        return obj == request.user
