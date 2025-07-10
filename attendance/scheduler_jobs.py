from django.core.management import call_command

def generate_monthly_attendance_job():
    call_command('generate_monthly_attendance')
