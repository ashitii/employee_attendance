from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from attendance.models import LeaveRequest, Notification
from django.core.paginator import Paginator
from datetime import date
import logging

logger = logging.getLogger(__name__)

def is_admin_or_manager(user):
    return user.groups.filter(name__in=['Admin', 'Manager']).exists()

@login_required
def leave_dashboard(request):
    if not request.user.groups.filter(name='Employee').exists() and not is_admin_or_manager(request.user):
        return redirect('login')

    try:
        if request.method == 'POST':
            start = request.POST.get('start_date')
            end = request.POST.get('end_date')
            leave_type = request.POST.get('leave_type')
            reason = request.POST.get('reason')

            LeaveRequest.objects.create(
                user=request.user,
                start_date=start,
                end_date=end,
                leave_type=leave_type,
                reason=reason,
                status='pending'
            )
            messages.success(request, "Leave request submitted successfully.")
            return redirect('leave_dashboard')

        leave_types = [lt[0] for lt in LeaveRequest.LEAVE_TYPE_CHOICES]

        sick_leaves = LeaveRequest.objects.filter(user=request.user, leave_type='Sick Leave')
        casual_leaves = LeaveRequest.objects.filter(user=request.user, leave_type='Casual Leave')
        work_from_home = LeaveRequest.objects.filter(user=request.user, leave_type='Work from Home')

        current_year = date.today().year
        sick_leaves_this_year = sick_leaves.filter(start_date__year=current_year)
        sick_leaves_used = sick_leaves_this_year.count()
        sick_leaves_remaining = 12 - sick_leaves_used

        context = {
            'sick_leaves': sick_leaves,
            'casual_leaves': casual_leaves,
            'work_from_home': work_from_home,
            'leave_types': leave_types,
            'sick_leaves_used': sick_leaves_used,
            'sick_leaves_remaining': sick_leaves_remaining,
        }
        return render(request, 'attendance/leave_dashboard.html', context)
    except Exception as e:
        logger.exception("Error in leave_dashboard")
        messages.error(request, "Failed to load leave dashboard.")
        return render(request, '500.html', status=500)

@login_required
def view_leave_requests(request):
    try:
        user = request.user

        if user.groups.filter(name='Admin').exists():
            leaves_qs = LeaveRequest.objects.all()
            can_approve = True
        elif user.groups.filter(name='Manager').exists():
            leaves_qs = LeaveRequest.objects.filter(user__groups__name='Employee')
            can_approve = True
        elif user.groups.filter(name='Employee').exists():
            leaves_qs = LeaveRequest.objects.filter(user=user)
            can_approve = False
        else:
            return redirect('login')

        paginator = Paginator(leaves_qs.order_by('-start_date'), 5)
        page_number = request.GET.get('page')
        leaves = paginator.get_page(page_number)

        context = {
            'leaves': leaves,
            'can_approve': can_approve
        }

        return render(request, 'attendance/leave_requests.html', context)
    except Exception as e:
        logger.exception("Error in view_leave_requests")
        messages.error(request, "Could not load leave requests.")
        return render(request, '500.html', status=500)

@login_required
@user_passes_test(is_admin_or_manager)
def update_leave_status(request, leave_id):
    try:
        if request.method == 'POST':
            leave = get_object_or_404(LeaveRequest, id=leave_id)
            action = request.POST.get('action')
            if action in ['Approved', 'Rejected']:
                if leave.status.lower() == 'pending':
                    leave.status = action.lower()
                    leave.save()
                    messages.success(request, f"Leave request {action.lower()} successfully.")
                    Notification.objects.create(
                        user=leave.user,
                        message=f"Your leave request from {leave.start_date} to {leave.end_date} was {action.lower()}."
                    )
                else:
                    messages.warning(request, "Leave request is already processed.")
            else:
                messages.error(request, "Invalid action.")
    except Exception as e:
        logger.exception("Error updating leave status")
        messages.error(request, "Could not update leave status.")
    return redirect('view_leave_requests')

@login_required
def delete_leave_request(request, leave_id):
    try:
        leave = get_object_or_404(LeaveRequest, id=leave_id)
        if request.user == leave.user or is_admin_or_manager(request.user):
            leave.delete()
            messages.success(request, "Leave request deleted successfully.")
        else:
            messages.error(request, "You don't have permission to delete this leave request.")
    except Exception as e:
        logger.exception("Error deleting leave request")
        messages.error(request, "Could not delete leave request.")
    return redirect('view_leave_requests')

@login_required
def change_leave_status(request, leave_id):
    try:
        if request.method == 'POST':
            leave = get_object_or_404(LeaveRequest, id=leave_id)
            new_status = request.POST.get('status')
            if new_status in ['approved', 'rejected']:
                leave.status = new_status
                leave.save()
                notif_msg = f"Your leave from {leave.start_date} to {leave.end_date} has been {new_status}."
                Notification.objects.create(user=leave.user, message=notif_msg)
                messages.success(request, "Leave status updated and notification sent.")
            else:
                messages.error(request, "Invalid status.")
    except Exception as e:
        logger.exception("Error changing leave status")
        messages.error(request, "Could not change leave status.")
    return redirect('view_leave_requests')
