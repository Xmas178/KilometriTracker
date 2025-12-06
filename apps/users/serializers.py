"""
User serializers for KilometriTracker API
Convert User model to/from JSON for API responses and requests

This file contains serializers for:
- User registration (creating new users)
- User profile (viewing/editing user info)
- User listing (admin view of all users)
"""

from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import User


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration

    Handles creating new user accounts. Validates password strength
    and ensures passwords match.

    Fields:
        - username: Unique username for login
        - email: User's email address
        - password: Password (write-only, never returned in API)
        - password2: Password confirmation (must match password)
        - first_name: User's first name (optional)
        - last_name: User's last name (optional)
        - company: Company name (optional)
        - phone: Phone number (optional)
    """

    # Extra field for password confirmation
    # This field is NOT in the User model, only used for validation
    password2 = serializers.CharField(
        write_only=True,  # Never include in API responses
        required=True,
        style={"input_type": "password"},  # Render as password field in browsable API
        help_text="Enter the same password again for verification",
    )

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "password",
            "password2",
            "first_name",
            "last_name",
            "company",
            "phone",
        ]
        extra_kwargs = {
            "password": {
                "write_only": True,  # Never return password in responses
                "style": {"input_type": "password"},
            },
            "email": {"required": True},  # Make email required for registration
        }

    def validate(self, attrs):
        """
        Validate the entire data dictionary

        Called after individual field validation.
        Used here to check if passwords match.

        Args:
            attrs (dict): Dictionary of all field values

        Returns:
            dict: Validated data

        Raises:
            ValidationError: If passwords don't match
        """

        # Check if password and password2 match
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )

        # Validate password strength using Django's built-in validators
        # This checks for common passwords, similarity to user info, etc.
        validate_password(attrs["password"])

        return attrs

    def create(self, validated_data):
        """
        Create and return a new User instance

        Called when serializer.save() is executed.
        Removes password2 and properly hashes the password.

        Args:
            validated_data (dict): Validated field values

        Returns:
            User: Created user instance
        """

        # Remove password2 from data (not a User model field)
        validated_data.pop("password2")

        # Create user with create_user() method
        # This method properly hashes the password (security!)
        # Never save password as plain text!
        user = User.objects.create_user(**validated_data)

        return user


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for user profile

    Used for viewing and updating user information.
    Does NOT include password field (use separate endpoint to change password).

    Read-only fields:
        - id: User's database ID
        - created_at: Account creation date
        - updated_at: Last profile update date
    """

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "company",
            "phone",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "username", "created_at", "updated_at"]
        # Note: username is read-only after creation (can't change username)


class UserListSerializer(serializers.ModelSerializer):
    """
    Serializer for user listing (minimal info)

    Used when listing multiple users (e.g., in admin panel).
    Shows only essential information for performance.

    This is lighter than UserSerializer - doesn't include all fields.
    """

    # Add computed field: full name
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["id", "username", "email", "full_name", "company", "created_at"]
        read_only_fields = ["id", "username", "created_at"]

    def get_full_name(self, obj):
        """
        Compute full name from first_name and last_name

        This is a SerializerMethodField - its value is computed
        by this method rather than taken directly from model.

        Method name must be: get_<field_name>

        Args:
            obj (User): User instance

        Returns:
            str: Full name or username if name not set
        """
        return obj.get_full_name()


class PasswordChangeSerializer(serializers.Serializer):
    """
    Serializer for changing password

    Separate endpoint for password changes (more secure).
    Requires old password to confirm user identity.

    Fields:
        - old_password: Current password (for verification)
        - new_password: New password
        - new_password2: New password confirmation
    """

    old_password = serializers.CharField(
        required=True,
        write_only=True,
        style={"input_type": "password"},
        help_text="Enter your current password",
    )

    new_password = serializers.CharField(
        required=True,
        write_only=True,
        style={"input_type": "password"},
        help_text="Enter your new password",
    )

    new_password2 = serializers.CharField(
        required=True,
        write_only=True,
        style={"input_type": "password"},
        help_text="Confirm your new password",
    )

    def validate_old_password(self, value):
        """
        Validate that old password is correct

        Args:
            value (str): Old password entered by user

        Returns:
            str: The old password (if valid)

        Raises:
            ValidationError: If old password is wrong
        """

        user = self.context["request"].user

        if not user.check_password(value):
            raise serializers.ValidationError("Old password is incorrect")

        return value

    def validate(self, attrs):
        """
        Validate that new passwords match and meet requirements

        Args:
            attrs (dict): All field values

        Returns:
            dict: Validated data

        Raises:
            ValidationError: If passwords don't match or are weak
        """

        # Check if new passwords match
        if attrs["new_password"] != attrs["new_password2"]:
            raise serializers.ValidationError(
                {"new_password": "New password fields didn't match."}
            )

        # Validate new password strength
        validate_password(attrs["new_password"])

        return attrs

    def save(self):
        """
        Save the new password

        Called when serializer.save() is executed.
        Updates user's password with proper hashing.

        Returns:
            User: Updated user instance
        """

        user = self.context["request"].user
        user.set_password(self.validated_data["new_password"])
        user.save()

        return user
