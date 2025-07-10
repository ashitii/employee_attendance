from django.db import models
from django.contrib.auth.models import User
from datetime import date

# --- Attendance Model ---
from datetime import datetime, timedelta, date as date_class

class Attendance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(default=date_class.today)
    clock_in = models.TimeField(null=True, blank=True)
    clock_out = models.TimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.date}"

    def total_working_hours(self):
        if self.clock_in and self.clock_out:
            # Combine date with time fields to create datetime objects
            dt_in = datetime.combine(self.date, self.clock_in)
            dt_out = datetime.combine(self.date, self.clock_out)
            duration = dt_out - dt_in
            # Format duration as hours and minutes
            hours, remainder = divmod(duration.total_seconds(), 3600)
            minutes = remainder // 60
            return f"{int(hours)}h {int(minutes)}m"
        return "-"






# --- Leave Request Model ---
class LeaveRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]
    LEAVE_TYPE_CHOICES = [
    ('Sick Leave', 'Sick Leave'),
    ('Casual Leave', 'Casual Leave'),
    ('Work from Home', 'Work from Home'),
    ('Emergency Leave', 'Emergency Leave'),
]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    leave_type = models.CharField(max_length=20, choices=LEAVE_TYPE_CHOICES, null=True, blank=True)
    reason = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

   
    def __str__(self):
        return f"{self.user.username} leave from {self.start_date} to {self.end_date} - {self.status}"

# --- Notification Model ---
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user.username}: {self.message[:20]}"
#Department


from django.db import models
from django.contrib.auth.models import User, Group

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    dob = models.DateField(null=True,blank=True)
    contact_number = models.CharField(max_length=15)
    
    # Department now linked to Django Group (e.g., Manager or Employee)
    department = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True, blank=True)
    profile_picture = models.ImageField(upload_to='static/profile_pics/', null=True, blank=True)


    def __str__(self):
        return self.user.username
    



class Holiday(models.Model):
    HOLIDAY_TYPE_CHOICES=[
        ('Company','Company Holiday'),
        ('Public','Public Holiday'),
        ('National','National Holiday'),    
        ('Festival','Festival Holiday'),
        ('Other','Other'),
    ]
    title = models.CharField(max_length=100)
    date = models.DateField()
    holiday_type=models.CharField(max_length=10,choices=HOLIDAY_TYPE_CHOICES)
    
    def __str__(self):
        return f"{self.title}-{self.date}"
    

from datetime import date


from django.db import models


class Notice(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    date_posted = models.DateField(auto_now_add=True)
    expiry_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.title
    
class BirthdayCard(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='birthdaycard')

    pdf= models.FileField(upload_to='birthday_cards/', null=True, blank=True)

    def __str__(self):
        return f"Birthday Card for {self.user.username}"
    

    from django.db import models
from django.contrib.auth.models import User

class MonthlyAttendanceRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    month = models.DateField(help_text='First day of the month')
    total_days_present = models.PositiveIntegerField(default=0)
    total_days_absent = models.PositiveIntegerField(default=0)
    total_working_hours = models.CharField(max_length=20, blank=True)
    generated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'month')
        ordering = ['-month']

    def __str__(self):
        return f"{self.user.username} - {self.month.strftime('%B %Y')}"


