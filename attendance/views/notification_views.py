from django.shortcuts import render
from django.http import JsonResponse, HttpResponseServerError
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from attendance.models import Notification
import logging

logger = logging.getLogger(__name__)

@login_required
def user_notifications(request):
    try:
        notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
        notifications.update(is_read=True)
        return render(request, 'attendance/notifications.html', {'notifications': notifications})
    except Exception as e:
        logger.exception("Error loading user notifications")
        return render(request, '500.html', status=500)

@login_required
def ajax_notifications(request):
    try:
        user = request.user
        notifications = Notification.objects.filter(user=user).order_by('-created_at')[:10]
        data = {
            'notifications': [
                {
                    'message': n.message,
                    'timestamp': n.created_at.strftime("%Y-%m-%d %H:%M")
                } for n in notifications
            ]
        }
        return JsonResponse(data)
    except Exception as e:
        logger.exception("Error fetching AJAX notifications")
        return JsonResponse({'error': 'Failed to load notifications'}, status=500)

@login_required
def notification_count(request):
    try:
        count = Notification.objects.filter(user=request.user, is_read=False).count()
        return JsonResponse({'unread_count': count})
    except Exception as e:
        logger.exception("Error getting notification count")
        return JsonResponse({'unread_count': 0, 'error': 'Failed to get count'}, status=500)

@require_POST
@login_required
def mark_notifications_read(request):
    try:
        Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
        return JsonResponse({'status': 'success'})
    except Exception as e:
        logger.exception("Error marking notifications as read")
        return JsonResponse({'status': 'error'}, status=500)
