"""
Report serializers for KilometriTracker API
Convert MonthlyReport model to/from JSON for API responses

This file contains serializers for:
- Monthly report viewing
- Report generation requests
"""

from rest_framework import serializers
from .models import MonthlyReport
from apps.core.validators import validate_year_month


class MonthlyReportSerializer(serializers.ModelSerializer):
    """
    Serializer for MonthlyReport model

    Used for viewing monthly reports.
    Includes all report fields plus computed display name.

    Read-only fields:
        - All fields are read-only (reports are generated, not manually created)
    """

    # Computed field: human-readable period (e.g., "December 2025")
    period_display = serializers.ReadOnlyField()

    # Display user as username instead of ID
    user_display = serializers.CharField(
        source="user.username", read_only=True, help_text="Username of report owner"
    )

    # File URLs (null if files not generated yet)
    pdf_url = serializers.SerializerMethodField()
    excel_url = serializers.SerializerMethodField()

    class Meta:
        model = MonthlyReport
        fields = [
            "id",
            "user",
            "user_display",
            "year",
            "month",
            "period_display",
            "total_km",
            "trip_count",
            "pdf_file",
            "pdf_url",
            "excel_file",
            "excel_url",
            "sent_at",
            "created_at",
        ]
        read_only_fields = "__all__"  # All fields are read-only

    def get_pdf_url(self, obj):
        """
        Get URL for PDF file

        Args:
            obj (MonthlyReport): Report instance

        Returns:
            str: URL to PDF file or None if not generated
        """
        if obj.pdf_file:
            request = self.context.get("request")
            if request:
                return request.build_absolute_uri(obj.pdf_file.url)
        return None

    def get_excel_url(self, obj):
        """
        Get URL for Excel file

        Args:
            obj (MonthlyReport): Report instance

        Returns:
            str: URL to Excel file or None if not generated
        """
        if obj.excel_file:
            request = self.context.get("request")
            if request:
                return request.build_absolute_uri(obj.excel_file.url)
        return None


class ReportGenerateSerializer(serializers.Serializer):
    """
    Serializer for report generation request

    Used when user requests to generate a report for specific month.
    This is NOT a MonthlyReport model serializer.

    Request body:
        {
            "year": 2025,
            "month": 12
        }

    Response:
        MonthlyReportSerializer data
    """

    year = serializers.IntegerField(
        min_value=2020, max_value=2030, help_text="Report year (e.g., 2025)"
    )

    month = serializers.IntegerField(
        min_value=1, max_value=12, help_text="Report month (1-12)"
    )

    def validate(self, attrs):
        """
        Validate year and month combination

        Args:
            attrs (dict): Field values

        Returns:
            dict: Validated data

        Raises:
            ValidationError: If year/month invalid
        """
        validate_year_month(attrs["year"], attrs["month"])
        return attrs
