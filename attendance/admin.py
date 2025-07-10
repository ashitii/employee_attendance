from django.contrib import admin
from django import forms

from .models import Attendance, Holiday, LeaveRequest, Notice, Notification, UserProfile
# from .models import Holiday
# Register your models here.




@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'clock_in', 'clock_out')
    list_filter = ('date', 'user')
    search_fields = ('user__username',)


@admin.register(LeaveRequest)
class LeaveRequestAdmin(admin.ModelAdmin):
    list_display = ('user', 'start_date', 'end_date', 'status')
    list_filter = ('status',)
    search_fields = ('user__username',)

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'is_read', 'created_at')
    search_fields = ('user__username',)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'contact_number', 'department')

@admin.register(Holiday)
class HolidayAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'holiday_type')
    list_filter = ('holiday_type',)

@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    list_display = ('title', 'date_posted', 'expiry_date')

from .models import BirthdayCard
admin.site.register(BirthdayCard)