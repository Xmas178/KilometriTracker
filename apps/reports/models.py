"""
Report models for KilometriTracker
Monthly travel reports with PDF/Excel export and email delivery

This file defines the MonthlyReport model which stores generated monthly
travel summary reports. Reports are automatically created at month-end
via Celery scheduled tasks.
"""

from django.db import models
from django.conf import settings


class MonthlyReport(models.Model):
    """
    Generated monthly travel report

    Represents a monthly summary of all trips for a specific user.
    Automatically generated at the end of each month by Celery task.

    Process:
    1. Celery task runs on last day of month
    2. Collects all user's trips for that month
    3. Calculates totals (km, trip count)
    4. Generates PDF and Excel files
    5. Sends email to user with attachments

    Fields:
        - user: Owner of this report (ForeignKey to User)
        - year: Report year (e.g., 2025)
        - month: Report month (1-12)
        - total_km: Sum of all trip distances for the month
        - trip_count: Number of trips in this report
        - pdf_file: Generated PDF report file
        - excel_file: Generated Excel report file
        - sent_at: When email was sent (NULL if not sent yet)
        - created_at: When this report was generated
    """

    # Link to user who owns this report
    # ForeignKey creates many-to-one relationship (many reports per user)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # Reference to custom User model
        on_delete=models.CASCADE,  # Delete reports if user deleted
        related_name="reports",  # Allows user.reports.all()
        help_text="Report owner",
    )

    # Year of the report (e.g., 2025)
    year = models.IntegerField(help_text="Report year (YYYY)")

    # Month of the report (1-12)
    # 1 = January, 2 = February, ..., 12 = December
    month = models.IntegerField(help_text="Report month (1-12)")

    # Total kilometers for the month
    # DecimalField for precise calculations
    # max_digits=10 allows up to 99,999,999.99 km (very generous!)
    # decimal_places=2 means 2 digits after decimal
    total_km = models.DecimalField(
        max_digits=10, decimal_places=2, help_text="Total kilometers for the month"
    )

    # Count of trips in this report
    trip_count = models.IntegerField(
        default=0, help_text="Number of trips in this report"
    )

    # Generated PDF file
    # FileField stores files in MEDIA_ROOT/reports/pdf/
    # upload_to specifies subdirectory within MEDIA_ROOT
    # null=True, blank=True means this field is optional
    pdf_file = models.FileField(
        upload_to="reports/pdf/",  # Saves to media/reports/pdf/
        null=True,  # Database allows NULL
        blank=True,  # Forms allow empty value
        help_text="Generated PDF report file",
    )

    # Generated Excel file
    # FileField stores files in MEDIA_ROOT/reports/excel/
    excel_file = models.FileField(
        upload_to="reports/excel/",  # Saves to media/reports/excel/
        null=True,
        blank=True,
        help_text="Generated Excel report file",
    )

    # Timestamp when email was sent
    # NULL means email not sent yet
    # DateTimeField allows storing date + time
    sent_at = models.DateTimeField(
        null=True, blank=True, help_text="Email sent timestamp"  # NULL if not sent yet
    )

    # Timestamp when report was created
    created_at = models.DateTimeField(
        auto_now_add=True,  # Set automatically on creation
        help_text="Report generation timestamp",
    )

    class Meta:
        """
        Model metadata - defines behavior and database settings
        """

        verbose_name = "Monthly Report"
        verbose_name_plural = "Monthly Reports"

        # Unique constraint: one report per user per month
        # Prevents duplicate reports for same user/month combination
        # Database will reject if you try to create duplicate
        unique_together = ("user", "year", "month")

        # Default ordering: newest reports first (by year desc, month desc)
        ordering = ["-year", "-month"]

        # Database index for faster queries
        # Composite index on (user, year DESC, month DESC)
        # Speeds up "get user's recent reports"
        indexes = [
            models.Index(fields=["user", "-year", "-month"]),
        ]

    def __str__(self):
        """
        String representation of report

        Returns human-readable description.
        Example: "sami - 2025/12 (607.50 km)"

        Returns:
            str: Report description with username, period, and total km
        """
        return (
            f"{self.user.username} - {self.year}/{self.month:02d} ({self.total_km} km)"
        )

    @property
    def period_display(self):
        """
        Return human-readable period string

        Property decorator makes this accessible as report.period_display
        Converts year/month to readable format.

        Example: year=2025, month=12 → "December 2025"

        Returns:
            str: Month name and year (e.g., "December 2025")
        """
        from datetime import date

        # Create date object for first day of month
        # strftime('%B') returns full month name (January, February, etc.)
        month_name = date(self.year, self.month, 1).strftime("%B")
        return f"{month_name} {self.year}"
