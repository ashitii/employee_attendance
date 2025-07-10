from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from attendance.models import Notice
from attendance.forms import NoticeForm
from django.core.paginator import Paginator
import logging

logger = logging.getLogger(__name__)

def is_admin(user):
    return user.groups.filter(name='Admin').exists()

@login_required
@user_passes_test(is_admin)
def manage_notices(request):
    try:
        notices = Notice.objects.all().order_by('-date_posted')
        paginator = Paginator(notices, 7)
        page_number = request.GET.get('page')
        notices = paginator.get_page(page_number)
        return render(request, 'attendance/manage_notices.html', {'notices': notices})
    except Exception as e:
        logger.exception("Failed to load notices.")
        messages.error(request, "An error occurred while loading notices.")
        return render(request, '500.html', status=500)

@login_required
@user_passes_test(is_admin)
def add_notice(request):
    try:
        form = NoticeForm(request.POST or None)
        if request.method == 'POST' and form.is_valid():
            form.save()
            messages.success(request, 'Notice added successfully.')
            return redirect('manage_notices')
        return render(request, 'attendance/add_notice.html', {'form': form, 'action': 'Add'})
    except Exception as e:
        logger.exception("Failed to add notice.")
        messages.error(request, "An error occurred while adding the notice.")
        return render(request, '500.html', status=500)

@login_required
@user_passes_test(is_admin)
def edit_notice(request, notice_id):
    try:
        notice = get_object_or_404(Notice, pk=notice_id)
        form = NoticeForm(request.POST or None, instance=notice)
        if request.method == 'POST' and form.is_valid():
            form.save()
            messages.success(request, 'Notice updated successfully.')
            return redirect('manage_notices')
        return render(request, 'attendance/edit_notice.html', {'form': form, 'action': 'Edit'})
    except Exception as e:
        logger.exception("Failed to edit notice.")
        messages.error(request, "An error occurred while editing the notice.")
        return render(request, '500.html', status=500)

@login_required
@user_passes_test(is_admin)
def delete_notice(request, notice_id):
    try:
        notice = get_object_or_404(Notice, pk=notice_id)
        notice.delete()
        messages.success(request, 'Notice deleted successfully.')
    except Exception as e:
        logger.exception("Failed to delete notice.")
        messages.error(request, "An error occurred while deleting the notice.")
    return redirect('manage_notices')
