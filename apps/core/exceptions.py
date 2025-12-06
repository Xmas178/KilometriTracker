"""
Custom exception handlers for KilometriTracker API
Provides consistent error response format across all API endpoints

This file defines:
1. Custom exception handler for DRF (Django REST Framework)
2. Custom exception classes for specific error cases
"""

from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
import logging

# Get logger for this module
logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    """
    Custom exception handler for Django REST Framework

    This function is called whenever an exception is raised in API views.
    It wraps DRF's default exception handler to provide a consistent
    error response format.

    Args:
        exc: The exception that was raised
        context: Context dict with info about where exception occurred

    Returns:
        Response: API response with standardized error format

    Response format:
        {
            "error": true,
            "message": "Human-readable error message",
            "status_code": 400,
            "details": {...}  # Optional additional details
        }
    """

    # Call DRF's default exception handler first
    # This handles common exceptions like ValidationError, PermissionDenied, etc.
    response = exception_handler(exc, context)

    if response is not None:
        # DRF recognized this exception and created a response
        # Now we customize the response format

        custom_response = {
            "error": True,
            "message": str(exc),  # Human-readable error message
            "status_code": response.status_code,
            "details": response.data,  # Original DRF error details
        }

        # Replace response data with our custom format
        response.data = custom_response

        # Log the error for debugging
        logger.error(
            f"API Error: {exc} | Status: {response.status_code} | "
            f"View: {context.get('view', 'Unknown')}"
        )
    else:
        # DRF didn't handle this exception (unexpected error)
        # Log it as a critical error
        logger.exception(
            f"Unhandled exception in API: {exc} | "
            f"View: {context.get('view', 'Unknown')}"
        )

    return response


# Custom exception classes for specific error cases


class GoogleMapsAPIError(Exception):
    """
    Raised when Google Maps Distance Matrix API fails

    This can happen due to:
    - Invalid API key
    - API quota exceeded
    - Network issues
    - Invalid addresses that Google can't find

    Usage:
        raise GoogleMapsAPIError("Failed to calculate distance: API quota exceeded")
    """

    pass


class InvalidAddressError(Exception):
    """
    Raised when address validation fails

    This can happen due to:
    - Address too short (< 5 characters)
    - Address too long (> 500 characters)
    - Address contains dangerous characters (SQL injection attempt)

    Usage:
        raise InvalidAddressError("Address must be at least 5 characters long")
    """

    pass


class ReportGenerationError(Exception):
    """
    Raised when monthly report generation fails

    This can happen due to:
    - No trips found for the month
    - PDF/Excel generation library errors
    - File system permission issues

    Usage:
        raise ReportGenerationError("No trips found for December 2025")
    """

    pass


class InsufficientDataError(Exception):
    """
    Raised when there's not enough data to perform an operation

    This can happen due to:
    - Trying to generate report with zero trips
    - Trying to calculate statistics without data

    Usage:
        raise InsufficientDataError("Cannot generate report: no trips in December 2025")
    """

    pass
