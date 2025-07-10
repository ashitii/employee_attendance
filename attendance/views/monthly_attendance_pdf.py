from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404
from attendance.models import MonthlyAttendanceRecord, Attendance
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from io import BytesIO
import datetime
import logging

logger = logging.getLogger(__name__)

@login_required
def monthly_attendance_pdf(request, record_id):
    try:
        record = MonthlyAttendanceRecord.objects.get(id=record_id)
    except MonthlyAttendanceRecord.DoesNotExist:
        logger.warning(f"MonthlyAttendanceRecord with ID {record_id} not found.")
        raise Http404("Record not found")

    try:
        month_start = record.month
        next_month = (month_start.replace(day=28) + datetime.timedelta(days=4)).replace(day=1)
        month_end = next_month - datetime.timedelta(days=1)

        daily_records = Attendance.objects.filter(
            user=record.user,
            date__range=(month_start, month_end)
        ).order_by('date')

        buffer = BytesIO()
        p = canvas.Canvas(buffer, pagesize=letter)
        width, height = letter
        y = height - 40

        p.setFont("Helvetica-Bold", 16)
        p.drawString(50, y, f"Monthly Attendance Report: {record.user.get_full_name() or record.user.username}")
        y -= 30
        p.setFont("Helvetica", 12)
        p.drawString(50, y, f"Month: {record.month.strftime('%B %Y')}")
        y -= 20
        p.drawString(50, y, f"Days Present: {record.total_days_present}")
        y -= 20
        p.drawString(50, y, f"Days Absent: {record.total_days_absent}")
        y -= 20
        p.drawString(50, y, f"Total Working Hours: {record.total_working_hours}")
        y -= 30
        p.setFont("Helvetica-Bold", 13)
        p.drawString(50, y, "Date        | Clock In | Clock Out | Working Hours")
        y -= 15
        p.setStrokeColor(colors.grey)
        p.line(50, y, width - 50, y)
        y -= 10
        p.setFont("Helvetica", 11)

        for att in daily_records:
            if y < 60:
                p.showPage()
                y = height - 40
                p.setFont("Helvetica-Bold", 13)
                p.drawString(50, y, "Date        | Clock In | Clock Out | Working Hours")
                y -= 15
                p.line(50, y, width - 50, y)
                y -= 10
                p.setFont("Helvetica", 11)

            work_hours = att.total_working_hours() if hasattr(att, 'total_working_hours') else "-"
            p.drawString(
                50, y,
                f"{att.date.strftime('%Y-%m-%d')}   {att.clock_in or '-'}      {att.clock_out or '-'}      {work_hours}"
            )
            y -= 18

        p.showPage()
        p.save()
        buffer.seek(0)

        filename = f"attendance_{record.user.username}_{record.month.strftime('%Y_%m')}.pdf"
        response = HttpResponse(buffer, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename={filename}'
        return response

    except Exception as e:
        logger.exception(f"Failed to generate PDF for MonthlyAttendanceRecord ID {record_id}")
        return HttpResponse("An error occurred while generating the PDF.", status=500)
