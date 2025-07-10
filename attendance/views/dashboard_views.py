from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils import timezone
from attendance.models import Attendance, LeaveRequest, Notice, UserProfile
from datetime import date
from django.db.models import Q
from django.core.paginator import Paginator
import logging

logger = logging.getLogger(__name__)

@login_required
def admin_dashboard(request):
    if not request.user.groups.filter(name='Admin').exists():
        return redirect('login')

    try:
        total_employees = User.objects.filter(groups__name='Employee').count()
        today_attendance = Attendance.objects.filter(date=timezone.now().date()).count()
        pending_leave_qs = LeaveRequest.objects.filter(status='pending')
        today = date.today()
        birthdays_today = UserProfile.objects.filter(dob__month=today.month, dob__day=today.day)

        all_users = User.objects.exclude(is_superuser=True).filter(
            groups__name__in=['Employee', 'Manager']
        ).distinct()
        role = request.GET.get('role')
        search = request.GET.get('search')
        if role:
            all_users = all_users.filter(groups__name=role)
        if search:
            all_users = all_users.filter(Q(username__icontains=search) | Q(email__icontains=search))

        context = {
            'total_employees': total_employees,
            'total_attendance': today_attendance,
            'pending_leaves': pending_leave_qs.count(),
            'leave_requests': pending_leave_qs,
            'birthdays_today': birthdays_today,
            'all_users': all_users,
        }
        return render(request, 'attendance/admin_dashboard.html', context)

    except Exception as e:
        logger.exception("Admin dashboard load failed")
        return render(request, '500.html', status=500)


@login_required
def manager_dashboard(request):
    if not request.user.groups.filter(name='Manager').exists():
        return redirect('login')

    try:
        attendance_qs = Attendance.objects.filter(user=request.user).order_by('-date')
        paginator = Paginator(attendance_qs, 10)
        page_number = request.GET.get('page')
        attendance_records = paginator.get_page(page_number)

        context = {
            'attendance_records': attendance_records,
        }

        notices = Notice.objects.filter(expiry_date__gte=date.today()) | Notice.objects.filter(expiry_date__isnull=True)
        context['notices'] = notices

        return render(request, 'attendance/manager_dashboard.html', context)

    except Exception as e:
        logger.exception("Manager dashboard load failed")
        return render(request, '500.html', status=500)


@login_required
def employee_dashboard(request):
    if not request.user.groups.filter(name='Employee').exists():
        return redirect('login')

    try:
        attendance_qs = Attendance.objects.filter(user=request.user).order_by('-date')
        paginator = Paginator(attendance_qs, 7)
        page_number = request.GET.get('page')
        attendance_records = paginator.get_page(page_number)

        context = {
            'attendance_records': attendance_records,
        }

        notices = Notice.objects.filter(expiry_date__gte=date.today()) | Notice.objects.filter(expiry_date__isnull=True)
        context['notices'] = notices

        return render(request, 'attendance/employee_dashboard.html', context)

    except Exception as e:
        logger.exception("Employee dashboard load failed")
        return render(request, '500.html', status=500)
