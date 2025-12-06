"""
URL routing for Users app
Maps URL patterns to view functions

This file defines all URL endpoints for user-related operations:
- Authentication (register, login, logout)
- Profile management
- User listing (admin)
"""

from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    UserRegistrationView,
    UserProfileView,
    UserDetailView,
    UserListView,
    PasswordChangeView,
    LogoutView,
)

# App namespace for URL reversing
# Usage: reverse('users:register') returns '/api/auth/register/'
app_name = "users"

urlpatterns = [
    # ========================================
    # Authentication Endpoints
    # ========================================
    # POST /api/auth/register/
    # Register new user account
    # Returns: user data + JWT tokens
    # Rate limit: 3 per hour per IP
    path("auth/register/", UserRegistrationView.as_view(), name="register"),
    # POST /api/auth/login/
    # Login with username + password
    # Returns: JWT access + refresh tokens
    # Body: {"username": "...", "password": "..."}
    path("auth/login/", TokenObtainPairView.as_view(), name="login"),
    # POST /api/auth/token/refresh/
    # Refresh access token using refresh token
    # Returns: new access token
    # Body: {"refresh": "..."}
    path("auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    # POST /api/auth/logout/
    # Logout (blacklist refresh token)
    # Body: {"refresh": "..."}
    # Rate limit: 10 per minute per user
    path("auth/logout/", LogoutView.as_view(), name="logout"),
    # POST /api/auth/change-password/
    # Change user password
    # Body: {"old_password": "...", "new_password": "...", "new_password2": "..."}
    # Rate limit: 3 per 15 minutes per user
    path("auth/change-password/", PasswordChangeView.as_view(), name="change_password"),
    # ========================================
    # Profile Endpoints
    # ========================================
    # GET /api/auth/profile/
    # View current user's profile
    # Returns: user data
    #
    # PUT/PATCH /api/auth/profile/
    # Update current user's profile
    # Body: {"first_name": "...", "company": "...", etc.}
    path("auth/profile/", UserProfileView.as_view(), name="profile"),
    # ========================================
    # User Management Endpoints (Admin)
    # ========================================
    # GET /api/users/
    # List all users (admin only)
    # Query params: ?search=..., ?ordering=..., ?company=...
    # Returns: list of users with minimal info
    path("users/", UserListView.as_view(), name="user_list"),
    # GET /api/users/<id>/
    # View specific user (self or admin)
    # Returns: user data
    #
    # PUT/PATCH /api/users/<id>/
    # Update specific user (self or admin)
    # Body: {"first_name": "...", etc.}
    #
    # DELETE /api/users/<id>/
    # Delete specific user (self or admin)
    path("users/<int:pk>/", UserDetailView.as_view(), name="user_detail"),
]
