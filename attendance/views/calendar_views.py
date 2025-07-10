from django.shortcuts import render
from django.http import JsonResponse
from datetime import datetime
import requests
from attendance.models import UserProfile
import logging

logger = logging.getLogger(__name__)

def calendar_view(request):
    return render(request, 'attendance/calendar.html')


def calendar_events(request):
    api_key = 'tcTuMSQ4qXaazxd6b5VN2kYr5wzOTdWy'
    year = datetime.now().year
    url = f"https://calendarific.com/api/v2/holidays?&api_key={api_key}&country=IN&year={year}"

    events = []

    # Fetch public holidays
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        for holiday in data.get('response', {}).get('holidays', []):
            events.append({
                'title': holiday['name'],
                'start': holiday['date']['iso'],
                'color': '#ff6666'
            })
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to fetch holidays from Calendarific API: {e}")
    except Exception as e:
        logger.exception("Unexpected error while processing holiday data")

    # Add birthdays
    try:
        profiles = UserProfile.objects.exclude(dob__isnull=True)
        for profile in profiles:
            birth_date = profile.dob.replace(year=year)
            name = f"{profile.user.first_name} {profile.user.last_name}"
            events.append({
                'title': f"{name}'s Birthday 🎉",
                'start': birth_date.isoformat(),
                'color': '#66ccff'
            })
    except Exception as e:
        logger.exception("Failed to load birthdays for calendar")

    return JsonResponse(events, safe=False)
