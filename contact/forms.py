from django import forms
from .models import GeneralEnquiry, Swarm


class GeneralEnquiryForm(forms.ModelForm):
    class Meta:
        model = GeneralEnquiry
        fields = ('contact_name_full', 'contact_email', 'contact_tel',
                  'enquiry_message',)

    def __init__(self, *args, **kwargs):
        """
        Add placeholders and classes, remove auto-generated
        labels and set autofocus on first field
        """
        super().__init__(*args, **kwargs)
        placeholders = {
            'contact_name_full': 'Full Name',
            'contact_email': 'Email Address',
            'contact_tel': 'Phone Number',
            'enquiry_message': 'Please enter your message here',
        }

        self.fields['contact_name_full'].widget.attrs['autofocus'] = True
        for field in self.fields:
            if self.fields[field].required:
                placeholder = f'{placeholders[field]} *'
            else:
                placeholder = placeholders[field]
            self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].widget.attrs['class'] = ('border-black '
                                                        'rounded-0 '
                                                        'contact-form-input')
            self.fields[field].label = False


class SwarmForm(forms.ModelForm):
    class Meta:
        model = Swarm
        fields = ('contact_name_full', 'contact_email', 'contact_tel',
                  'swarm_street_address1', 'swarm_street_address2',
                  'swarm_city', 'swarm_county', 'swarm_country',
                  'swarm_postcode', 'swarm_message',)

    def __init__(self, *args, **kwargs):
        """
        Add placeholders and classes, remove auto-generated
        labels and set autofocus on first field
        """
        super().__init__(*args, **kwargs)
        placeholders = {
            'contact_name_full': 'Full Name',
            'contact_email': 'Email Address',
            'contact_tel': 'Phone Number',
            'swarm_street_address1': 'Address, Line 1',
            'swarm_street_address2': 'Address, Line 2',
            'swarm_city': 'City',
            'swarm_county': 'County',
            'swarm_postcode': 'Post Code',
            'swarm_message':
                'Please enter useful information about the swarm, such as: '
                'Location on property, approximate height, how long the swarm'
                'has been there, if bees are flying or clustered, etc',
        }

        self.fields['contact_name_full'].widget.attrs['autofocus'] = True
        for field in self.fields:
            if field != 'swarm_country':
                if self.fields[field].required:
                    placeholder = f'{placeholders[field]} *'
                else:
                    placeholder = placeholders[field]
                self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].widget.attrs['class'] = ('border-black '
                                                        'rounded-0 '
                                                        'contact-form-input')
            self.fields[field].label = False
