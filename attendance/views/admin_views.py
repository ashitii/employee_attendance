from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_POST
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib import messages
import logging

logger = logging.getLogger(__name__)

@csrf_protect
@require_POST
@user_passes_test(lambda u: u.is_superuser)
def change_user_role(request, user_id):
    try:
        user = get_object_or_404(User, id=user_id)
        new_role = request.POST.get('role')
        employee_group = Group.objects.get(name='Employee')
        manager_group = Group.objects.get(name='Manager')

        user.groups.clear()

        if new_role == 'Manager':
            user.groups.add(manager_group)
        else:
            user.groups.add(employee_group)

        user.save()
        messages.success(request, f"User role updated to {new_role}.")
    except Group.DoesNotExist as e:
        logger.error(f"Group not found: {e}")
        messages.error(request, "Required group does not exist.")
    except Exception as e:
        logger.exception("Unexpected error in change_user_role")
        messages.error(request, "Something went wrong while updating the user role.")
    return redirect('admin_dashboard')


@login_required
def admin_dashboard(request):
    try:
        all_users = User.objects.exclude(is_superuser=True).filter(
            groups__name__in=['Employee', 'Manager']
        ).distinct()
        context = {
            'all_users': all_users,
        }
        return render(request, 'attendance/admin_dashboard.html', context)
    except Exception as e:
        logger.exception("Error loading admin dashboard")
        messages.error(request, "Failed to load admin dashboard.")
        return render(request, '500.html', status=500)


def is_admin(user):
    return user.groups.filter(name='Admin').exists()
