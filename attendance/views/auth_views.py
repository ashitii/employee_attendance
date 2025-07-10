from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from attendance.forms import UserForm, UserProfileForm
from django.contrib.auth.models import Group
import logging

logger = logging.getLogger(__name__)

def user_login(request):
    try:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Logged in successfully!')
                if user.groups.filter(name='Admin').exists():
                    return redirect('admin_dashboard')
                elif user.groups.filter(name='Manager').exists():
                    return redirect('manager_dashboard')
                elif user.groups.filter(name='Employee').exists():
                    return redirect('employee_dashboard')
                else:
                    messages.error(request, 'User does not belong to any group.')
                    return redirect('login')
            else:
                messages.error(request, 'Invalid username or password')
    except Exception as e:
        logger.exception("Login error")
        messages.error(request, 'An unexpected error occurred during login.')
    return render(request, 'attendance/login.html')


def user_logout(request):
    try:
        logout(request)
        messages.success(request, "You have been logged out.")
    except Exception as e:
        logger.exception("Logout error")
        messages.error(request, "An error occurred during logout.")
    return redirect('login')


def register(request):
    try:
        if request.method == 'POST':
            user_form = UserForm(request.POST)
            profile_form = UserProfileForm(request.POST)

            if user_form.is_valid() and profile_form.is_valid():
                user = user_form.save()
                profile = profile_form.save(commit=False)
                profile.user = user

                dob_input = profile_form.cleaned_data.get("dob")
                if dob_input in ["", None, "unknown"]:
                    profile.dob = None
                else:
                    profile.dob = dob_input

                profile.save()

                selected_group = profile_form.cleaned_data.get('department')
                if selected_group:
                    user.groups.add(selected_group)

                messages.success(request, 'Registration successful. Login to enter.')
                return redirect('login')
        else:
            user_form = UserForm()
            profile_form = UserProfileForm()
    except Exception as e:
        logger.exception("Registration error")
        messages.error(request, "An error occurred during registration.")
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request, 'attendance/register.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })
