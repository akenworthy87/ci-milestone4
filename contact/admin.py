from django.contrib import admin
from .models import GeneralEnquiry, Swarm


class GeneralEnquiryAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'contact_date',
        'user_profile',
        'contact_name_full',
    )


class SwarmAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'contact_date',
        'user_profile',
        'contact_name_full',
    )


admin.site.register(GeneralEnquiry, GeneralEnquiryAdmin)
admin.site.register(Swarm, SwarmAdmin)
