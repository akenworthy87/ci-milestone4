from django.contrib import admin
from .models import Order, OrderLineItem, OrderStatus


class OrderStatusAdmin(admin.ModelAdmin):
    list_display = (
        'status_friendly',
        'status_code',
    )


class OrderLineItemAdminInline(admin.TabularInline):
    model = OrderLineItem
    readonly_fields = ('lineitem_total',)


class OrderAdmin(admin.ModelAdmin):
    inlines = (OrderLineItemAdminInline,)

    readonly_fields = ('order_number', 'order_date',
                       'cost_delivery', 'cost_total',
                       'cost_grand_total', 'original_bag',
                       'stripe_pid',)

    fields = ('order_number', 'order_status', 'user_profile',
              'order_date', 'name_full', 'email', 'tel',
              'street_address1', 'street_address2', 'city',
              'county', 'country', 'postcode',
              'cost_delivery', 'cost_total', 'cost_grand_total',
              'original_bag', 'stripe_pid',)

    list_display = ('order_number', 'order_status', 'order_date', 'name_full',
                    'cost_total', 'cost_delivery', 'cost_grand_total',)

    ordering = ('-order_date',)


admin.site.register(OrderStatus, OrderStatusAdmin)
admin.site.register(Order, OrderAdmin)
