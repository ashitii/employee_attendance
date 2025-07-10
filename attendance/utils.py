import logging
from django.core.paginator import Paginator



def paginate_queryset(request, queryset, per_page=10):
    """
    Paginates a queryset based on the request and returns the page object.

    Args:
        request: The HTTP request object containing pagination parameters.
        queryset: The queryset to paginate.
        per_page: Number of items per page (default is 10).

    Returns:
        A page object containing the paginated results.
    """
    paginator = Paginator(queryset, per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj
    

import os
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings

# utils.py

# Function to send birthday email with optional PDF attachment

def send_birthday_email(user, pdf_path):
    subject = "🎉 Happy Birthday from Zynova Solutions!"
    message = f"Dear {user.first_name},\n\nWishing you a very Happy Birthday!\n\nEnjoy your special day!\n\n– Team Zynova"
    
    try:
        email = EmailMessage(
            subject=subject,
            body=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[user.email],
        )

        if pdf_path and os.path.exists(pdf_path):
            email.attach_file(pdf_path)
        
        email.send()
        return True  # success flag
    except Exception as e:
        # Log the error (optional but recommended)
        logging.error(f"Error sending birthday email to {user.email}: {e}")
        return False  # failure flag