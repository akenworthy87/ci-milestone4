from django.db import models
from django_countries.fields import CountryField

from profiles.models import UserProfile


class GeneralEnquiry(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.SET_NULL,
                                     null=True, blank=True,
                                     related_name='general_enqs')
    contact_name_full = models.CharField(max_length=50,
                                         null=False, blank=False)
    contact_email = models.EmailField(max_length=254, null=False, blank=False)
    contact_tel = models.CharField(max_length=20, null=False, blank=False)
    contact_date = models.DateTimeField(auto_now_add=True)
    enquiry_message = models.TextField()

    def __str__(self):
        return str(self.id)


class Swarm(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.SET_NULL,
                                     null=True, blank=True,
                                     related_name='swarms')
    contact_name_full = models.CharField(max_length=50,
                                         null=False, blank=False)
    contact_email = models.EmailField(max_length=254, null=False, blank=False)
    contact_tel = models.CharField(max_length=20, null=False, blank=False)
    contact_date = models.DateTimeField(auto_now_add=True)
    swarm_street_address1 = models.CharField(max_length=80,
                                             null=False, blank=False)
    swarm_street_address2 = models.CharField(max_length=80,
                                             null=True, blank=True)
    swarm_county = models.CharField(max_length=80, null=True, blank=True)
    swarm_town_or_city = models.CharField(max_length=40, null=False,
                                          blank=False)
    swarm_country = CountryField(blank_label='Country *', null=False,
                                 blank=False)
    swarm_postcode = models.CharField(max_length=20, null=True, blank=True)
    swarm_message = models.TextField()

    def __str__(self):
        return str(self.id)
