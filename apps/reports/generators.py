"""
PDF report generator for KilometriTracker
Generates professional PDF reports with trip data and statistics

This module creates PDF reports containing:
- Report header with user info and period
- Trip table with all trips for the month
- Total kilometers summary
- Generation timestamp
"""

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.enums import TA_CENTER, TA_RIGHT
from datetime import datetime
from decimal import Decimal
import io


class PDFReportGenerator:
    """
    PDF report generator using ReportLab

    Creates professional travel reports with formatted tables
    and automatic page breaks.
    """

    def __init__(self):
        """Initialize PDF generator with styles"""
        self.styles = getSampleStyleSheet()

        # Create custom title style
        self.title_style = ParagraphStyle(
            "CustomTitle",
            parent=self.styles["Heading1"],
            fontSize=24,
            textColor=colors.HexColor("#2C3E50"),
            spaceAfter=30,
            alignment=TA_CENTER,
        )

        # Create custom heading style
        self.heading_style = ParagraphStyle(
            "CustomHeading",
            parent=self.styles["Heading2"],
            fontSize=14,
            textColor=colors.HexColor("#34495E"),
            spaceAfter=12,
            spaceBefore=12,
        )

    def generate_report(self, report, trips, output_path):
        """
        Generate PDF report

        Args:
            report (MonthlyReport): Report instance
            trips (QuerySet): Trip queryset for the month
            output_path (str): Full path where PDF will be saved

        Returns:
            str: Path to generated PDF file
        """

        # Create PDF document
        doc = SimpleDocTemplate(
            output_path,
            pagesize=A4,
            rightMargin=2 * cm,
            leftMargin=2 * cm,
            topMargin=2 * cm,
            bottomMargin=2 * cm,
        )

        # Container for PDF elements
        elements = []

        # Add title
        title = Paragraph(f"Travel Report - {report.period_display}", self.title_style)
        elements.append(title)
        elements.append(Spacer(1, 0.5 * cm))

        # Add user info
        user_info = Paragraph(
            f"<b>Traveler:</b> {report.user.get_full_name()}<br/>"
            f"<b>Company:</b> {report.user.company or 'N/A'}<br/>"
            f"<b>Email:</b> {report.user.email}",
            self.styles["Normal"],
        )
        elements.append(user_info)
        elements.append(Spacer(1, 0.8 * cm))

        # Add trip table
        if trips.exists():
            elements.append(self._create_trip_table(trips))
            elements.append(Spacer(1, 0.5 * cm))

            # Add summary
            elements.append(self._create_summary(report))
        else:
            no_trips = Paragraph(
                "<i>No trips recorded for this period.</i>", self.styles["Normal"]
            )
            elements.append(no_trips)

        elements.append(Spacer(1, 1 * cm))

        # Add footer with generation date
        footer = Paragraph(
            f"<i>Report generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}</i>",
            ParagraphStyle(
                "Footer",
                parent=self.styles["Normal"],
                fontSize=8,
                textColor=colors.grey,
                alignment=TA_RIGHT,
            ),
        )
        elements.append(footer)

        # Build PDF
        doc.build(elements)

        return output_path

    def _create_trip_table(self, trips):
        """
        Create formatted table with trip data

        Args:
            trips (QuerySet): Trip queryset

        Returns:
            Table: ReportLab Table object
        """

        # Table header
        data = [["Date", "From", "To", "Distance (km)", "Purpose"]]

        # Add trip rows
        for trip in trips:
            data.append(
                [
                    trip.date.strftime("%Y-%m-%d"),
                    (
                        trip.start_address[:30] + "..."
                        if len(trip.start_address) > 30
                        else trip.start_address
                    ),
                    (
                        trip.end_address[:30] + "..."
                        if len(trip.end_address) > 30
                        else trip.end_address
                    ),
                    f"{trip.distance_km:.2f}",
                    (
                        trip.purpose[:25] + "..."
                        if trip.purpose and len(trip.purpose) > 25
                        else (trip.purpose or "-")
                    ),
                ]
            )

        # Create table
        table = Table(data, colWidths=[3 * cm, 5 * cm, 5 * cm, 3 * cm, 4 * cm])

        # Style table
        table.setStyle(
            TableStyle(
                [
                    # Header styling
                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#3498DB")),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("FONTSIZE", (0, 0), (-1, 0), 10),
                    ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                    # Data rows styling
                    ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
                    ("TEXTCOLOR", (0, 1), (-1, -1), colors.black),
                    ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
                    ("FONTSIZE", (0, 1), (-1, -1), 9),
                    ("ALIGN", (3, 1), (3, -1), "RIGHT"),  # Align distance to right
                    # Grid
                    ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                    # Alternating row colors
                    (
                        "ROWBACKGROUNDS",
                        (0, 1),
                        (-1, -1),
                        [colors.white, colors.lightgrey],
                    ),
                    # Padding
                    ("TOPPADDING", (0, 1), (-1, -1), 6),
                    ("BOTTOMPADDING", (0, 1), (-1, -1), 6),
                    ("LEFTPADDING", (0, 0), (-1, -1), 8),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ]
            )
        )

        return table

    def _create_summary(self, report):
        """
        Create summary section with totals

        Args:
            report (MonthlyReport): Report instance

        Returns:
            Table: ReportLab Table with summary
        """

        data = [
            ["Total Trips:", str(report.trip_count)],
            ["Total Distance:", f"{report.total_km:.2f} km"],
        ]

        summary_table = Table(data, colWidths=[8 * cm, 4 * cm])

        summary_table.setStyle(
            TableStyle(
                [
                    ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
                    ("FONTNAME", (1, 0), (1, -1), "Helvetica-Bold"),
                    ("FONTSIZE", (0, 0), (-1, -1), 12),
                    ("ALIGN", (1, 0), (1, -1), "RIGHT"),
                    ("TEXTCOLOR", (0, 0), (-1, -1), colors.HexColor("#2C3E50")),
                    ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#ECF0F1")),
                    ("GRID", (0, 0), (-1, -1), 1, colors.HexColor("#BDC3C7")),
                    ("TOPPADDING", (0, 0), (-1, -1), 8),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                    ("LEFTPADDING", (0, 0), (-1, -1), 12),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 12),
                ]
            )
        )

        return summary_table
