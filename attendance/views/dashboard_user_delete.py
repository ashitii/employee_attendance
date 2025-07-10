from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
import logging

logger = logging.getLogger(__name__)

@login_required
def dashboard_user_delete(request, user_id):
    if not request.user.is_superuser and not request.user.groups.filter(name='Admin').exists():
        return redirect('admin_dashboard')

    if request.method == 'POST':
        try:
            user = User.objects.filter(id=user_id).first()
            if user:
                username = user.username
                user.delete()
                messages.success(request, f"User '{username}' deleted successfully.")
            else:
                messages.warning(request, "User not found.")
        except Exception as e:
            logger.exception("Error deleting user with ID %s", user_id)
            messages.error(request, "An error occurred while deleting the user.")

    return redirect('admin_dashboard')
