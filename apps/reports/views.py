"""
Report views for KilometriTracker API
Handle monthly report viewing and generation

This file contains API endpoints for:
- Monthly report listing
- Report detail viewing
- Report generation (basic, no PDF/Excel yet)
"""

from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Sum
from decimal import Decimal

from .models import MonthlyReport
from .serializers import MonthlyReportSerializer, ReportGenerateSerializer
from apps.trips.models import Trip
from apps.core.permissions import IsOwner
import logging

logger = logging.getLogger(__name__)


class MonthlyReportListView(generics.ListAPIView):
    """
    API endpoint for listing monthly reports

    GET /api/reports/

    List all reports for authenticated user.
    Sorted by newest first (year/month descending).
    """

    serializer_class = MonthlyReportSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Return reports for current user only"""
        return MonthlyReport.objects.filter(user=self.request.user).order_by(
            "-year", "-month"
        )


class MonthlyReportDetailView(generics.RetrieveAPIView):
    """
    API endpoint for viewing specific monthly report

    GET /api/reports/<id>/

    View details of specific report.
    User can only view their own reports.
    """

    serializer_class = MonthlyReportSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        """Return reports for current user only"""
        return MonthlyReport.objects.filter(user=self.request.user)


class GenerateReportView(APIView):
    """
    API endpoint for generating monthly report

    POST /api/reports/generate/

    Generate monthly report for specific month.
    Creates MonthlyReport object with summary data.

    NOTE: PDF/Excel generation will be added later.
    For MVP, this just creates the report record.
    """

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        """Handle POST request - generate monthly report"""

        # Validate request data
        serializer = ReportGenerateSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        year = serializer.validated_data["year"]
        month = serializer.validated_data["month"]
        user = request.user

        # Check if report already exists
        existing_report = MonthlyReport.objects.filter(
            user=user, year=year, month=month
        ).first()

        if existing_report:
            logger.warning(f"Report already exists for {user.username} {year}/{month}")
            return Response(
                {
                    "error": f"Report for {year}/{month:02d} already exists",
                    "report": MonthlyReportSerializer(
                        existing_report, context={"request": request}
                    ).data,
                },
                status=status.HTTP_409_CONFLICT,
            )

        # Get trips for this month
        trips = Trip.objects.filter(user=user, date__year=year, date__month=month)

        trip_count = trips.count()

        if trip_count == 0:
            logger.info(f"No trips found for {user.username} {year}/{month}")
            return Response(
                {
                    "error": f"No trips found for {year}/{month:02d}. "
                    f"Cannot generate empty report."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Calculate total kilometers
        total_km = trips.aggregate(total=Sum("distance_km"))["total"] or Decimal("0.00")

        # Create report
        report = MonthlyReport.objects.create(
            user=user, year=year, month=month, total_km=total_km, trip_count=trip_count
        )

        # TODO: Generate PDF and Excel files here (future feature)

        logger.info(
            f"Report generated for {user.username}: "
            f"{year}/{month} - {trip_count} trips, {total_km} km"
        )

        # Serialize and return
        response_serializer = MonthlyReportSerializer(
            report, context={"request": request}
        )

        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
