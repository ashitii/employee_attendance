from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.auth.models import User
from attendance.models import MonthlyAttendanceRecord
from datetime import date
import logging

logger = logging.getLogger(__name__)

@login_required
def monthly_attendance_view(request):
    try:
        user = request.user
        month = request.GET.get('month')

        if user.is_superuser or user.groups.filter(name__in=['Admin', 'Manager']).exists():
            records = MonthlyAttendanceRecord.objects.select_related('user').order_by('-month', 'user__username')
        else:
            records = MonthlyAttendanceRecord.objects.filter(user=user).order_by('-month')

        if month:
            try:
                year, month_num = map(int, month.split('-'))
                records = records.filter(month__year=year, month__month=month_num)
            except ValueError:
                logger.warning(f"Invalid month format received: {month}")
                records = MonthlyAttendanceRecord.objects.none()

    except Exception as e:
        logger.exception("Failed to load monthly attendance records")
        records = MonthlyAttendanceRecord.objects.none()

    return render(request, 'attendance/monthly_attendance.html', {'records': records})
