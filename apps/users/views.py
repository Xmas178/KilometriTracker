"""
User views for KilometriTracker API
Handle user registration, authentication, and profile management

This file contains API endpoints for:
- User registration (create new account)
- User profile viewing/updating
- Password change
- User listing (admin only)
"""

from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django_ratelimit.decorators import ratelimit
from django.utils.decorators import method_decorator
from django.contrib.auth import get_user_model
from .serializers import (
    UserRegistrationSerializer,
    UserSerializer,
    UserListSerializer,
    PasswordChangeSerializer,
)
from apps.core.permissions import IsSelfOrAdmin

User = get_user_model()


@method_decorator(ratelimit(key="ip", rate="3/h", method="POST"), name="dispatch")
class UserRegistrationView(generics.CreateAPIView):
    """
    API endpoint for user registration
    Rate limit: 3 registrations per hour per IP address
    This prevents automated account creation and spam.

    POST /api/auth/register/

    Anyone can register (no authentication required).
    Returns user data and JWT tokens on successful registration.

    Request body:
        {
            "username": "sami",
            "email": "sami@example.com",
            "password": "securepassword123",
            "password2": "securepassword123",
            "first_name": "Sami",
            "last_name": "Lammi",
            "company": "CodeNob Dev",
            "phone": "+358 123 456789"
        }

    Response (201 Created):
        {
            "user": {
                "id": 1,
                "username": "sami",
                "email": "sami@example.com",
                ...
            },
            "tokens": {
                "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
                "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
            },
            "message": "User registered successfully"
        }
    """

    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]  # Anyone can register

    def create(self, request, *args, **kwargs):
        """
        Handle POST request - create new user

        Overridden to include JWT tokens in response.

        Args:
            request: HTTP request object

        Returns:
            Response: User data + JWT tokens
        """

        # Validate and save user using serializer
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Generate JWT tokens for the new user
        refresh = RefreshToken.for_user(user)

        # Prepare response data
        response_data = {
            "user": UserSerializer(user).data,
            "tokens": {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            },
            "message": "User registered successfully",
        }

        return Response(response_data, status=status.HTTP_201_CREATED)


class UserProfileView(generics.RetrieveUpdateAPIView):
    """
    API endpoint for viewing and updating user profile

    GET /api/auth/profile/
    PUT/PATCH /api/auth/profile/

    Users can view and update their own profile.
    Admins can view and update any user's profile.

    GET Response (200 OK):
        {
            "id": 1,
            "username": "sami",
            "email": "sami@example.com",
            "first_name": "Sami",
            "last_name": "Lammi",
            "company": "CodeNob Dev",
            "phone": "+358 123 456789",
            "created_at": "2025-12-06T20:00:00Z",
            "updated_at": "2025-12-06T20:00:00Z"
        }

    PUT/PATCH Request:
        {
            "first_name": "Sami",
            "last_name": "Updated",
            "company": "New Company"
        }
    """

    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """
        Return the current user's profile

        Returns:
            User: Currently authenticated user
        """
        return self.request.user


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint for viewing/updating/deleting specific user (admin or self)

    GET /api/users/<id>/
    PUT/PATCH /api/users/<id>/
    DELETE /api/users/<id>/

    Users can access their own profile.
    Admins can access any user's profile.

    This is different from UserProfileView:
    - UserProfileView: /profile/ (always current user)
    - UserDetailView: /users/<id>/ (specific user by ID)
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, IsSelfOrAdmin]


class UserListView(generics.ListAPIView):
    """
    API endpoint for listing all users (admin only)

    GET /api/users/

    Returns list of all users with minimal information.
    Only accessible by admin users.

    Response (200 OK):
        [
            {
                "id": 1,
                "username": "sami",
                "email": "sami@example.com",
                "full_name": "Sami Lammi",
                "company": "CodeNob Dev",
                "created_at": "2025-12-06T20:00:00Z"
            },
            ...
        ]

    Query parameters:
        - search: Search by username, email, or company
        - ordering: Sort by field (e.g., -created_at for newest first)
    """

    queryset = User.objects.all()
    serializer_class = UserListSerializer
    permission_classes = [permissions.IsAdminUser]

    # Enable filtering and searching
    filterset_fields = ["company", "is_staff", "is_active"]
    search_fields = ["username", "email", "first_name", "last_name", "company"]
    ordering_fields = ["username", "email", "created_at"]
    ordering = ["-created_at"]  # Default: newest first


@method_decorator(ratelimit(key="user", rate="3/15m", method="POST"), name="dispatch")
class PasswordChangeView(APIView):
    """
    API endpoint for changing password
    Rate limit: 3 attempts per 15 minutes per user
    This prevents brute-force password attacks.

    POST /api/auth/change-password/

    User must be authenticated.
    Requires old password for security.

    Request body:
        {
            "old_password": "currentpassword123",
            "new_password": "newsecurepassword456",
            "new_password2": "newsecurepassword456"
        }

    Response (200 OK):
        {
            "message": "Password changed successfully"
        }

    Error Response (400 Bad Request):
        {
            "old_password": ["Old password is incorrect"]
        }
    """

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        """
        Handle POST request - change password

        Args:
            request: HTTP request object

        Returns:
            Response: Success or error message
        """

        # Validate password change data
        serializer = PasswordChangeSerializer(
            data=request.data, context={"request": request}
        )

        if serializer.is_valid():
            # Save new password
            serializer.save()

            return Response(
                {"message": "Password changed successfully"}, status=status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@method_decorator(ratelimit(key="user", rate="10/m", method="POST"), name="dispatch")
class LogoutView(APIView):
    """
    API endpoint for user logout

    POST /api/auth/logout/

    Rate limit: 10 logouts per minute per user
    This prevents logout spam.

    Blacklists the refresh token so it can't be used again.
    This prevents token reuse after logout.

    Request body:
        {
            "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
        }

    Response (200 OK):
        {
            "message": "Logged out successfully"
        }

    Note: Access tokens continue to work until they expire (1 hour).
    This is normal JWT behavior. For maximum security, clients
    should delete both tokens immediately on logout.
    """

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        """
        Handle POST request - logout user

        Args:
            request: HTTP request object

        Returns:
            Response: Success or error message
        """
        try:
            # Get refresh token from request
            refresh_token = request.data.get("refresh")

            if not refresh_token:
                return Response(
                    {"error": "Refresh token is required"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Blacklist the refresh token
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(
                {"message": "Logged out successfully"}, status=status.HTTP_200_OK
            )

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
