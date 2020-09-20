from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib import messages

from profiles.models import UserProfile


def post_actions(request, form):
    """
    A shared function to handle attaching the user profile to
    a message record and saving it.
    Returns false if form invalid.
    If form valid, attempts to attach user profile to record if
    user logged in and has profile, returns saved form (with record id).
    """
    if form.is_valid():
        if request.user.is_authenticated:
            profile = UserProfile.objects.get(user=request.user)
            # Attach the user's profile to the form
            form = form.save(commit=False)
            form.user_profile = profile
        form.save()
        messages.success(request, 'Message sent successfully')
        return form
    else:
        messages.error(request,
                       ('Message failed. Please ensure '
                        'the form is valid.'))
        return False


def send_message_confirmation_email(message, ref):
    """Send the user a confirmation email"""
    cust_email = message.contact_email
    contact_email = settings.DEFAULT_FROM_EMAIL
    subject = render_to_string(
        'contact/confirmation_emails/confirmation_email_subject.txt',
        {'message': message, 'ref': ref})
    body = render_to_string(
        'contact/confirmation_emails/confirmation_email_body.txt',
        {'message': message, 'contact_email': contact_email})

    send_mail(
        subject,
        body,
        settings.DEFAULT_FROM_EMAIL,
        [cust_email]
    )


def send_swarms_list_email(message, ref):
    """Send the user a confirmation email"""
    swarm_list_email = settings.DEFAULT_SWARMS_EMAIL
    contact_email = settings.DEFAULT_FROM_EMAIL
    subject = render_to_string(
        'contact/swarm_emails/new_swarm_subject.txt',
        {'message': message, 'ref': ref})
    body = render_to_string(
        'contact/swarm_emails/new_swarm_body.txt',
        {'message': message, 'contact_email': contact_email})

    send_mail(
        subject,
        body,
        settings.DEFAULT_FROM_EMAIL,
        [swarm_list_email]
    )
