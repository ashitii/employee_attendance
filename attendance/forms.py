from django import forms
from django.contrib.auth.models import Group
from .models import (
    Attendance, UserProfile, Holiday, Notice
)
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class UserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].widget.attrs.update({
            'placeholder': 'Enter your username',
            'class': 'form-control'
        })
        self.fields['first_name'].widget.attrs.update({
            'placeholder': 'Enter your first name',
            'class': 'form-control'
        })
        self.fields['last_name'].widget.attrs.update({
            'placeholder': 'Enter your last name',
            'class': 'form-control'
        })
        self.fields['email'].widget.attrs.update({
            'placeholder': 'Enter your email address',
            'class': 'form-control'
        })
        self.fields['password1'].widget.attrs.update({
            'placeholder': 'Enter your password',
            'class': 'form-control'
        })
        self.fields['password2'].widget.attrs.update({
            'placeholder': 'Confirm your password',
            'class': 'form-control'
        })

class UserProfileForm(forms.ModelForm):
    dob = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )

    department = forms.ModelChoiceField(
        queryset=Group.objects.filter(name__in=['Manager', 'Employee']),
        empty_label="Select Department",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = UserProfile
        fields = ['dob', 'contact_number', 'department']
        widgets = {
            'contact_number': forms.TextInput(attrs={'placeholder': 'Enter contact number', 'class': 'form-control'}),
        }

##############3edit profile
class EditUserForm(forms.ModelForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter your email address',
    }))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your username'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your first name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your last name'}),
        }

class EditUserProfileForm(forms.ModelForm):
    dob = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    contact_number = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter contact number'})
    )
    department = forms.ModelChoiceField(
        queryset=Group.objects.filter(name__in=['Manager', 'Employee']),
        required=False,
        empty_label="Select Department",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    profile_picture = forms.ImageField(
        required=False,
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = UserProfile
        fields = ['dob', 'contact_number', 'department', 'profile_picture']


# attendance/forms.py



class NoticeForm(forms.ModelForm):
    class Meta:
        model = Notice
        fields = ['title', 'description', 'expiry_date']
        widgets = {
            'expiry_date': forms.DateInput(attrs={'type': 'date'})
        }


class HolidayForm(forms.ModelForm):
    HOLIDAY_TYPE_CHOICES = [
        ("Public", "Public Holiday"),
        ("Company", "Company Holiday"),
        ("National", "National Holiday"),
        ("Festival", "Festival Holiday"),
        ("Other", "Other"),
    ]
    holiday_type = forms.ChoiceField(
        choices=HOLIDAY_TYPE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True
    )
    class Meta:
        model = Holiday
        fields = ['title', 'date', 'holiday_type']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }
        
        
class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = '__all__'
        widgets = {
            'clock_in': forms.TimeInput(format='%H:%M:%S', attrs={'type': 'time'}),
            'clock_out': forms.TimeInput(format='%H:%M:%S', attrs={'type': 'time'}),
        }


from django import forms
from .models import BirthdayCard

class BirthdayCardForm(forms.ModelForm):
    class Meta:
        model = BirthdayCard
        fields = ['pdf']
