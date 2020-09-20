from django.shortcuts import render, redirect, reverse

from .forms import GeneralEnquiryForm, SwarmForm
from .utils import post_actions, send_message_confirmation_email, send_swarms_list_email
from profiles.models import UserProfile


def contact(request):
    """ Displays the contact form """

    if request.method == 'POST':
        form = GeneralEnquiryForm(request.POST)
        message = post_actions(request, form)
        # If message submission fails, post_actions returns false.
        # Below and skips the else on L19.
        # Submitted form is passed back to render with error message.
        if message:
            send_message_confirmation_email(message, "GEN")
            return redirect(reverse('home'))
    else:
        # Attempt to prefill the form with any info
        # the user maintains in their profile
        if request.user.is_authenticated:
            try:
                profile = UserProfile.objects.get(user=request.user)
                form = GeneralEnquiryForm(initial={
                    'contact_name_full': profile.user.get_full_name(),
                    'contact_email': profile.user.email,
                    'contact_tel': profile.user_tel,
                })
            except UserProfile.DoesNotExist:
                form = GeneralEnquiryForm()
        else:
            form = GeneralEnquiryForm()

    template = 'contact/contact.html'
    context = {
        'form': form,
    }

    return render(request, template, context)


def swarms(request):
    """ Displays the swarm report form """

    if request.method == 'POST':
        form = SwarmForm(request.POST)
        message = post_actions(request, form)
        if message:
            send_message_confirmation_email(message, "swm")
            send_swarms_list_email(message, "swm")
            return redirect(reverse('home'))
    else:
        # Attempt to prefill the form with any info
        # the user maintains in their profile
        if request.user.is_authenticated:
            try:
                profile = UserProfile.objects.get(user=request.user)
                form = SwarmForm(initial={
                    'contact_name_full': profile.user.get_full_name(),
                    'contact_email': profile.user.email,
                    'contact_tel': profile.user_tel,
                })
            except UserProfile.DoesNotExist:
                form = SwarmForm()
        else:
            form = SwarmForm()

    template = 'contact/swarms.html'
    context = {
        'form': form,
    }

    return render(request, template, context)
