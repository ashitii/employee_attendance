from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from attendance.models import Holiday
from attendance.forms import HolidayForm

@login_required
# @user_passes_test(lambda u:u.groups.filter(name='Admin').exists())
def holiday_list(request):
    holidays=Holiday.objects.all().order_by('date')
    return render(request,'attendance/holiday_list.html',{'holidays':holidays})

@login_required
@user_passes_test(lambda u:u.groups.filter(name='Admin').exists())
def add_holiday(request):
    try:
        if request.method == 'POST':
            form = HolidayForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('holiday_list')  # 🔁 Prevent re-submission on refresh
        else:
            form = HolidayForm()
        return render(request, 'attendance/add_holiday.html', {'form': form})
    except Exception as e:
        from django.contrib import messages
        import logging
        logger = logging.getLogger(__name__)
        logger.exception("Error adding holiday")
        messages.error(request, "Failed to add holiday. Please try again.")
        return render(request, 'attendance/add_holiday.html', {'form': HolidayForm()})