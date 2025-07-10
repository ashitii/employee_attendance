from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from attendance.views.monthly_attendance_views import monthly_attendance_view
from attendance.views.monthly_attendance_pdf import monthly_attendance_pdf
# from attendance.views.user_delete_list import user_delete_list
# from attendance.views.quick_user_delete import quick_user_delete
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.shortcuts import redirect
from attendance.views.dashboard_user_delete import dashboard_user_delete
from attendance.views.dashboard_views import admin_dashboard, manager_dashboard  # <-- Use dashboard_views version
from attendance.views.force_error import force_error

urlpatterns = [
    path('', views.user_login, name='login'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/',views.register, name="register"),
    path('calendar/',views.calendar_view, name="calendar"),
    path('calendar/events/',views.calendar_events, name="calendar_events"),
    path('edit_profile/',views.edit_profile, name="edit_profile"),
    path('dashboard/', admin_dashboard, name='admin_dashboard'),
    path('manager-dashboard/', manager_dashboard, name='manager_dashboard'),
    path('dashboard/delete-user/<int:user_id>/', dashboard_user_delete, name='dashboard_user_delete'),
    # path('dashboard/quick-user-delete/', quick_user_delete, name='quick_user_delete'),
    path('employee-dashboard/', views.employee_dashboard, name='employee_dashboard'),

    path('clock-in/', views.clock_in, name='clock_in'),
    path('clock-out/', views.clock_out, name='clock_out'),

     path('leave-dashboard/', views.leave_dashboard, name='leave_dashboard'),

    path('leave-requests/', views.view_leave_requests, name='view_leave_requests'),
    path('leave/update-status/<int:leave_id>/', views.update_leave_status, name='update_leave_status'),
    path('leave/delete/<int:leave_id>/', views.delete_leave_request, name='delete_leave_request'),

    path('notifications/', views.user_notifications, name='notifications'),
        # ... other paths ...
    path('notifications/ajax/', views.ajax_notifications, name='ajax_notifications'),
    path('notifications/count/', views.notification_count, name='notification_count'),
    path('notifications/mark-read/', views.mark_notifications_read, name='mark_notifications_read'),

    #forget password
    path('password_reset/',auth_views.PasswordResetView.as_view(template_name='attendance/password_reset_form.html'),name='password_reset'),
    path('password_reset_done/',auth_views.PasswordResetDoneView.as_view(template_name='attendance/password_reset_done.html'),name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='attendance/password_reset_confirm.html'),name='password_reset_confirm'),
    path('password_reset_complete/',auth_views.PasswordResetCompleteView.as_view(template_name='attendance/password_reset_complete.html'),name='password_reset_complete'),
    
    path('holidays/', views.holiday_list, name='holiday_list'),
    path('holidays/add/', views.add_holiday, name='add_holiday'),
    

    path('upload-birthday-card/<int:user_id>/', views.upload_birthday_card, name='upload_birthday_card'),


    # notices
    path('notices/', views.manage_notices, name='manage_notices'),
    path('notices/add/', views.add_notice, name='add_notice'),
    path('notices/edit/<int:notice_id>/', views.edit_notice, name='edit_notice'),
    path('notices/delete/<int:notice_id>/', views.delete_notice, name='delete_notice'),
    
    path('monthly-attendance/', monthly_attendance_view, name='monthly_attendance'),
    path('monthly-attendance/pdf/<int:record_id>/', monthly_attendance_pdf, name='monthly_attendance_pdf'),

    # path('admin/users/', user_delete_list, name='user_delete_list'),
    # path('admin/users/delete/<int:user_id>/', csrf_exempt(lambda request, user_id: (User.objects.filter(id=user_id).delete(), redirect('user_delete_list'))[1] if request.method == 'POST' else redirect('user_delete_list')), name='delete_user'),
    path('force500/',force_error, name='force500'),

]

