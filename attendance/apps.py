import sys
from django.apps import AppConfig
import logging


class AttendanceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'attendance'

    def ready(self):
        # Only start scheduler if running server, not during migrations, shell, or management commands
        if any(cmd in sys.argv for cmd in ['makemigrations', 'migrate', 'shell', 'collectstatic', 'test']):
            return
        if not any(cmd in sys.argv[0] or cmd in sys.argv for cmd in ['runserver', 'daphne', 'uvicorn']):
            return
        from apscheduler.schedulers.background import BackgroundScheduler
        from apscheduler.triggers.cron import CronTrigger
        from django_apscheduler.jobstores import DjangoJobStore

        scheduler = BackgroundScheduler()
        scheduler.add_jobstore(DjangoJobStore(), 'default')
        # Restore to run only on the 1st of each month at 00:05
        scheduler.add_job(
            'attendance.scheduler_jobs:generate_monthly_attendance_job',
            trigger=CronTrigger(day=1, hour=0, minute=5),
            id='monthly_attendance_job',
            replace_existing=True,
        )
        scheduler.start()
        logging.getLogger(__name__).info('APScheduler started for monthly attendance generation.')
