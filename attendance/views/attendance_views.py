from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages
from attendance.models import Attendance
import logging

logger = logging.getLogger(__name__)

def is_admin_or_manager(user):
    return user.groups.filter(name__in=['Admin', 'Manager']).exists()

@login_required
def clock_in(request):
    if not is_admin_or_manager(request.user) and not request.user.groups.filter(name='Employee').exists():
        return redirect('login')

    try:
        today = timezone.now().date()
        if not Attendance.objects.filter(user=request.user, date=today).exists():
            now = timezone.localtime().time()
            Attendance.objects.create(user=request.user, clock_in=now, date=today)
            messages.success(request, "Clocked in successfully!")
        else:
            messages.warning(request, "You have already clocked in.")
    except Exception as e:
        logger.exception("Clock-in error")
        messages.error(request, "An error occurred while clocking in.")

    return redirect('manager_dashboard' if request.user.groups.filter(name='Manager').exists() else 'employee_dashboard')


@login_required
def clock_out(request):
    if not is_admin_or_manager(request.user) and not request.user.groups.filter(name='Employee').exists():
        return redirect('login')

    today = timezone.now().date()
    try:
        attendance = Attendance.objects.get(user=request.user, date=today)
        if not attendance.clock_out:
            now = timezone.localtime().time()
            attendance.clock_out = now
            attendance.save()
            messages.success(request, "Clocked out successfully!")
        else:
            messages.warning(request, "You have already clocked out.")
    except Attendance.DoesNotExist:
        messages.error(request, "You must clock in first.")
    except Exception as e:
        logger.exception("Clock-out error")
        messages.error(request, "An unexpected error occurred while clocking out.")

    return redirect('manager_dashboard' if request.user.groups.filter(name='Manager').exists() else 'employee_dashboard')
