from django.shortcuts import render  # , get_object_or_404
from django.contrib import messages

# from .models import GeneralEnquiry, Swarm
from .forms import GeneralEnquiryForm
from profiles.models import UserProfile
# from profiles.forms import UserProfileForm


def contact(request):
    """ Display the user's profile. """

    if request.method == 'POST':
        form = GeneralEnquiryForm(request.POST)

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
        else:
            messages.error(request,
                           ('Message failed. Please ensure '
                            'the form is valid.'))
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
        'on_profile_page': True
    }

    return render(request, template, context)


def swarms(request):
    return
