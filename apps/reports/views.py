"""
URL routing for Reports app
Maps URL patterns to view functions

This file defines all URL endpoints for report-related operations:
- Monthly report listing
- Report generation
"""

from django.urls import path
from .views import MonthlyReportListView, MonthlyReportDetailView, GenerateReportView

# App namespace for URL reversing
app_name = "reports"

urlpatterns = [
    # GET /api/reports/
    # List all monthly reports for authenticated user
    path("reports/", MonthlyReportListView.as_view(), name="report_list"),
    # GET /api/reports/<id>/
    # View specific monthly report
    path("reports/<int:pk>/", MonthlyReportDetailView.as_view(), name="report_detail"),
    # POST /api/reports/generate/
    # Generate new monthly report
    # Body: {"year": 2025, "month": 12}
    path("reports/generate/", GenerateReportView.as_view(), name="generate_report"),
]
