# utils.py or views/birthday_email_utils.py
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

def send_birthday_email(user, card):
    subject = f"🎉 Happy Birthday {user.first_name}!"
    message = render_to_string('emails/birthday_email.html', {'user': user})

    email = EmailMessage(
        subject=subject,
        body=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[user.email],
    )

    # Attach the file with a unique name per user
    filename = f"HBD_{user.username}.pdf"
    with open(card, 'rb') as f:
        email.attach(filename, f.read(), 'application/pdf')

    email.content_subtype = 'html'
    email.send()
# views.py
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from attendance.forms import BirthdayCardForm
from attendance.models import BirthdayCard, User
# from attendance.views.birthday_email_views import send_birthday_email  
from attendance.utils import send_birthday_email

@login_required
@user_passes_test(lambda u: u.groups.filter(name='Admin').exists())
def upload_birthday_card(request, user_id):
    try:
        user = get_object_or_404(User, pk=user_id)
        card, created = BirthdayCard.objects.get_or_create(user=user)

        if request.method == 'POST':
            form = BirthdayCardForm(request.POST, request.FILES, instance=card)
            if form.is_valid():
                card = form.save()
                pdf_path = card.pdf.path if card.pdf else None
                send_birthday_email(user, pdf_path)
                messages.success(request, f"🎉 Birthday email sent to {user.get_full_name()}!")
                return redirect('admin_dashboard')
        else:
            form = BirthdayCardForm(instance=card)
    except Exception as e:
        logger.exception("Error uploading or emailing birthday card")
        messages.error(request, "Something went wrong while processing the birthday card.")

    return render(request, 'attendance/upload_card.html', {
        'form': form,
        'birthday_user': user
    })