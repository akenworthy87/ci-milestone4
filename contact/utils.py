from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib import messages

from profiles.models import UserProfile


def post_actions(request, form):
    """
    A shared function to handle attaching the user profile to
    a message record and saving it.
    """
    if form.is_valid():
        if request.user.is_authenticated:
            profile = UserProfile.objects.get(user=request.user)
            # Attach the user's profile to the form
            linked_user = form.save(commit=False)
            linked_user.user_profile = profile
            linked_user.save()
        else:
            form.save()
        messages.success(request, 'Message sent successfully')
        return True
    else:
        messages.error(request,
                       ('Message failed. Please ensure '
                        'the form is valid.'))
        return False


def send_message_confirmation_email(message):
    """Send the user a confirmation email"""
    cust_email = message.contact_email
    subject = render_to_string(
        'contact/confirmation_emails/confirmation_email_subject.txt',
        {'message': message})
    body = render_to_string(
        'contact/confirmation_emails/confirmation_email_body.txt',
        {'message': message, 'contact_email': settings.DEFAULT_FROM_EMAIL})

    send_mail(
        subject,
        body,
        settings.DEFAULT_FROM_EMAIL,
        [cust_email]
    )