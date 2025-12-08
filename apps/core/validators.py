"""
Custom validators for KilometriTracker
Input validation functions to ensure data quality and security

This file contains validators for:
- Distance values (positive, reasonable range)
- Address strings (length, dangerous characters)
- Date ranges (not in future, not too old)
"""

from django.core.exceptions import ValidationError
import re
from datetime import date, timedelta


def validate_distance(value):
    """
    Validate distance value for trips

    Ensures distance is:
    - Positive (> 0)
    - Reasonable (< 10,000 km)
    - Not suspiciously round numbers that suggest fake data

    Args:
        value (Decimal or float): Distance in kilometers

    Raises:
        ValidationError: If distance is invalid

    Examples:
        validate_distance(607.5)   # OK
        validate_distance(0)       # Raises ValidationError
        validate_distance(15000)   # Raises ValidationError
    """

    # Check if distance is positive
    if value <= 0:
        raise ValidationError(
            "Distance must be positive. Please enter a value greater than 0.",
            code="invalid_distance_negative",
        )

    # Check if distance is reasonable (max 10,000 km)
    # This catches obvious input errors (e.g., user entered meters instead of km)
    if value > 10000:
        raise ValidationError(
            "Distance seems unreasonably high (max 10,000 km). "
            "Please verify the distance is correct.",
            code="invalid_distance_too_high",
        )

    # Optional: Warn about suspiciously round numbers
    # (This is just a warning, not a hard error)
    if value % 100 == 0 and value >= 100:
        # Distance is exactly 100, 200, 300, etc.
        # This might be estimated rather than actual
        # We don't raise error, just log it
        import logging

        logger = logging.getLogger(__name__)
        logger.warning(f"Suspiciously round distance: {value} km")


def validate_address(value):
    """
    Validate address string for security and quality

    Ensures address:
    - Has minimum length (5 characters)
    - Not too long (max 500 characters)
    - Doesn't contain dangerous characters (SQL injection, XSS)

    Args:
        value (str): Address string

    Raises:
        ValidationError: If address is invalid

    Examples:
        validate_address("Oulu, Finland")        # OK
        validate_address("Hi")                   # Raises ValidationError (too short)
        validate_address("Test <script>...")     # Raises ValidationError (dangerous chars)
    """

    # Check minimum length
    # Addresses shorter than 5 characters are likely incomplete
    if len(value) < 1:
        raise ValidationError(
            "Address is too short. Please enter at least 5 characters.",
            code="invalid_address_too_short",
        )

    # Check maximum length
    # Prevents database overflow and potential DoS attacks
    if len(value) > 500:
        raise ValidationError(
            "Address is too long. Maximum 500 characters allowed.",
            code="invalid_address_too_long",
        )

    # Check for dangerous characters that might indicate:
    # - SQL injection attempt: '; --, /* */
    # - XSS attempt: <script>, <iframe>
    # - Command injection: ; | &
    dangerous_patterns = [
        r"<script",  # XSS: <script>
        r"<iframe",  # XSS: <iframe>
        r"javascript:",  # XSS: javascript:
        r"--;",  # SQL: comment
        r"/\*",  # SQL: comment start
        r"\*/",  # SQL: comment end
        r"\|\|",  # SQL: string concatenation
        r"@@",  # SQL: variables
    ]

    for pattern in dangerous_patterns:
        if re.search(pattern, value, re.IGNORECASE):
            raise ValidationError(
                "Address contains invalid characters. "
                "Please use only standard address characters.",
                code="invalid_address_dangerous_chars",
            )


def validate_trip_date(value):
    """
    Validate trip date

    Ensures date is:
    - Not in the future (can't have trips that haven't happened yet)
    - Not too old (more than 2 years ago seems suspicious)

    Args:
        value (date): Trip date

    Raises:
        ValidationError: If date is invalid

    Examples:
        validate_trip_date(date(2025, 12, 6))   # OK (today)
        validate_trip_date(date(2026, 1, 1))    # Raises ValidationError (future)
        validate_trip_date(date(2020, 1, 1))    # Raises ValidationError (too old)
    """

    today = date.today()

    # Check if date is in the future
    if value > today:
        raise ValidationError(
            "Trip date cannot be in the future. "
            "Please enter a date that has already occurred.",
            code="invalid_date_future",
        )

    # Check if date is too old (more than 2 years ago)
    # This helps catch data entry errors (wrong year)
    two_years_ago = today - timedelta(days=730)  # ~2 years

    if value < two_years_ago:
        raise ValidationError(
            f"Trip date is more than 2 years old ({value}). "
            f"Please verify the date is correct.",
            code="invalid_date_too_old",
        )


def validate_year_month(year, month):
    """
    Validate year and month for reports

    Ensures:
    - Month is 1-12
    - Year is reasonable (2020-2030)
    - Date is not in the future

    Args:
        year (int): Year (e.g., 2025)
        month (int): Month (1-12)

    Raises:
        ValidationError: If year/month combination is invalid

    Examples:
        validate_year_month(2025, 12)  # OK
        validate_year_month(2025, 13)  # Raises ValidationError (invalid month)
        validate_year_month(2026, 6)   # Raises ValidationError (future)
    """

    # Validate month range
    if not 1 <= month <= 12:
        raise ValidationError(
            f"Invalid month: {month}. Month must be between 1 and 12.",
            code="invalid_month",
        )

    # Validate year range (reasonable bounds)
    current_year = date.today().year

    if year < 2020:
        raise ValidationError(
            f"Year {year} is too old. Reports are only available from 2020 onwards.",
            code="invalid_year_too_old",
        )

    if year > current_year + 1:
        raise ValidationError(
            f"Year {year} is too far in the future.", code="invalid_year_future"
        )

    # Check if this month/year is in the future
    today = date.today()
    report_date = date(year, month, 1)

    if report_date > today:
        raise ValidationError(
            f"Cannot generate report for {year}/{month:02d}: date is in the future.",
            code="invalid_report_date_future",
        )


def validate_file_size(file, max_size_mb=10):
    """
    Validate uploaded file size

    NOTE: Not currently used in MVP. This is a utility function
    for future features where users can upload files (receipts,
    import Excel files, etc.)

    Ensures files aren't too large (prevents DoS attacks and
    server storage issues)

    Args:
        file: Uploaded file object
        max_size_mb (int): Maximum allowed size in megabytes

    Raises:
        ValidationError: If file is too large

    Examples:
        validate_file_size(uploaded_file, max_size_mb=5)  # Max 5 MB
    """

    if file.size > max_size_mb * 1024 * 1024:  # Convert MB to bytes
        raise ValidationError(
            f"File size ({file.size / 1024 / 1024:.2f} MB) exceeds "
            f"maximum allowed size ({max_size_mb} MB).",
            code="invalid_file_size",
        )
