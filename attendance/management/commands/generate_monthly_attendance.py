from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from attendance.models import Attendance, MonthlyAttendanceRecord
from datetime import date, timedelta
from django.db.models import Q

class Command(BaseCommand):
    help = 'Generate monthly attendance records for all users at month end.'

    def handle(self, *args, **kwargs):
        today = date.today()
        # Get the first day of the current month
        first_day = today.replace(day=1)
        # Get the last day of the previous month
        last_month = first_day - timedelta(days=1)
        month_start = last_month.replace(day=1)
        month_end = last_month

        for user in User.objects.all():
            attendances = Attendance.objects.filter(user=user, date__range=(month_start, month_end))
            total_days_present = attendances.count()
            total_days_absent = (month_end - month_start).days + 1 - total_days_present
            total_working_seconds = 0
            for att in attendances:
                if att.clock_in and att.clock_out:
                    dt_in = att.clock_in.hour * 3600 + att.clock_in.minute * 60
                    dt_out = att.clock_out.hour * 3600 + att.clock_out.minute * 60
                    total_working_seconds += max(0, dt_out - dt_in)
            hours = total_working_seconds // 3600
            minutes = (total_working_seconds % 3600) // 60
            total_working_hours = f"{int(hours)}h {int(minutes)}m"
            MonthlyAttendanceRecord.objects.update_or_create(
                user=user,
                month=month_start,
                defaults={
                    'total_days_present': total_days_present,
                    'total_days_absent': total_days_absent,
                    'total_working_hours': total_working_hours,
                }
            )
        self.stdout.write(self.style.SUCCESS('Monthly attendance records generated.'))
