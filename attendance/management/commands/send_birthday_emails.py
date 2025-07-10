from django.core.management.base import BaseCommand
from django.utils import timezone
from attendance.models import UserProfile
from attendance.views.birthday_email_views import send_birthday_email

class Command(BaseCommand):
    help = 'Send birthday wishes to users whose birthday is today.'

    def handle(self, *args, **kwargs):
        today = timezone.localdate()
        birthday_profiles = UserProfile.objects.filter(
            dob__day=today.day,
            dob__month=today.month
        )

        if not birthday_profiles.exists():
            self.stdout.write("🎈 No birthdays today.")
            return

        for profile in birthday_profiles:
            send_birthday_email(profile.user)
            self.stdout.write(self.style.SUCCESS(f"🎉 Sent birthday email to {profile.user.email}"))
            