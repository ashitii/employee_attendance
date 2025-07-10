from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from attendance.forms import EditUserForm, EditUserProfileForm
from django.contrib import messages
import logging

logger = logging.getLogger(__name__)

@login_required
def edit_profile(request):
    user = request.user

    try:
        if request.method == 'POST':
            user_form = EditUserForm(request.POST, instance=user)
            profile_form = EditUserProfileForm(request.POST, request.FILES, instance=user.userprofile)

            if user_form.is_valid() and profile_form.is_valid():
                user_form.save()
                profile_form.save()
                messages.success(request, "Profile updated successfully.")

                # Redirect based on group
                if user.groups.filter(name='Manager').exists():
                    return redirect('manager_dashboard')
                elif user.groups.filter(name='Employee').exists():
                    return redirect('employee_dashboard')
                elif user.groups.filter(name='Admin').exists():
                    return redirect('admin_dashboard')
                else:
                    return redirect('admin_dashboard')
            else:
                messages.error(request, "Please correct the errors in the form.")
        else:
            user_form = EditUserForm(instance=user)
            profile_form = EditUserProfileForm(instance=user.userprofile)

    except Exception as e:
        logger.exception("Error occurred while editing profile")
        messages.error(request, "Something went wrong while updating your profile.")
        user_form = EditUserForm(instance=user)
        profile_form = EditUserProfileForm(instance=user.userprofile)

    return render(request, 'attendance/edit_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form,
    })
