from django.http import HttpResponse
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

from .models import Order, OrderLineItem, OrderStatus
from products.models import ProductStock
from profiles.models import UserProfile

import json
import time

from stripe import PaymentIntent


class StripeWH_Handler:
    """Handle Stripe webhooks"""

    def __init__(self, request):
        self.request = request

    def _send_confirmation_email(self, order):
        """Send the user a confirmation email"""
        cust_email = order.email
        subject = render_to_string(
            'checkout/confirmation_emails/confirmation_email_subject.txt',
            {'order': order})
        body = render_to_string(
            'checkout/confirmation_emails/confirmation_email_body.txt',
            {'order': order, 'contact_email': settings.DEFAULT_FROM_EMAIL})

        send_mail(
            subject,
            body,
            settings.DEFAULT_FROM_EMAIL,
            [cust_email]
        )

    def handle_event(self, event):
        """
        Handle a generic/unknown/unexpected webhook event
        """
        return HttpResponse(
            content=f'Unhandled webhook received: {event["type"]}',
            status=200)

    def handle_payment_intent_amount_capturable_updated(self, event):
        """
        Handle the payment_intent.amount_capturable_updated webhook from Stripe
        """
        intent = event.data.object
        pid = intent.id
        bag = intent.metadata.bag
        save_info = intent.metadata.save_info

        billing_details = intent.charges.data[0].billing_details
        shipping_details = intent.shipping
        grand_total = round(intent.charges.data[0].amount / 100, 2)

        # Clean data in the shipping details
        for field, value in shipping_details.address.items():
            if value == "":
                shipping_details.address[field] = None

        # Update profile information if save_info was checked
        profile = None
        username = intent.metadata.username
        if username != 'AnonymousUser':
            profile = UserProfile.objects.get(user__username=username)
            if save_info:
                profile.user_tel = shipping_details.phone
                profile.user_street_address1 = shipping_details.address.line1
                profile.user_street_address2 = shipping_details.address.line2
                profile.user_city = shipping_details.address.city
                profile.user_county = shipping_details.address.state
                profile.user_postcode = shipping_details.address.postal_code
                profile.user_country = shipping_details.address.country
                profile.save()

        order_exists = False
        attempt = 1
        # Tries to find existing order, attempts 5 times
        while attempt <= 5:
            try:
                order = Order.objects.get(
                    name_full__iexact=shipping_details.name,
                    email__iexact=billing_details.email,
                    tel__iexact=shipping_details.phone,
                    street_address1__iexact=shipping_details.address.line1,
                    street_address2__iexact=shipping_details.address.line2,
                    city__iexact=shipping_details.address.city,
                    county__iexact=shipping_details.address.state,
                    country__iexact=shipping_details.address.country,
                    postcode__iexact=shipping_details.address.postal_code,
                    cost_grand_total=grand_total,
                    original_bag=bag,
                    stripe_pid=pid,
                )
                order_exists = True
                break
            except Order.DoesNotExist:
                attempt += 1
                time.sleep(1)
        # If order found: changes status to 'Pending', send email confirmation
        if order_exists:
            pending_status = OrderStatus.objects.get(status_code="pending")
            order.order_status = pending_status
            order.save()
            self._send_confirmation_email(order)
            return HttpResponse(
                content=(f'Webhook received: {event["type"]} | SUCCESS: '
                         'Verified order already in database'),
                status=200)
        # If order not found: attempts to create it
        else:
            order = None
            pending_status = OrderStatus.objects.get(status_code="pending")
            try:
                # Sets order details
                order = Order.objects.create(
                    name_full=shipping_details.name,
                    user_profile=profile,
                    order_status=pending_status,
                    creation_method='Webhook',
                    email=billing_details.email,
                    tel=shipping_details.phone,
                    street_address1=shipping_details.address.line1,
                    street_address2=shipping_details.address.line2,
                    city=shipping_details.address.city,
                    county=shipping_details.address.state,
                    country=shipping_details.address.country,
                    postcode=shipping_details.address.postal_code,
                    original_bag=bag,
                    stripe_pid=pid,
                )
                # Attaches order line items
                for item_id, item_data in json.loads(bag).items():
                    product_line = ProductStock.objects.get(id=item_id)
                    product_line.reserve_stock(item_data)
                    order_line_item = OrderLineItem(
                        order=order,
                        product_line=product_line,
                        quantity=item_data,
                    )
                    order_line_item.save()
            # Deletes order if anything goes wrong
            except ValueError as e:
                if order:
                    order.delete()
                PaymentIntent.cancel(pid, cancellation_reason='abandoned')
                return HttpResponse(
                    content=f'Webhook received: {event["type"]} | ERROR: {e}',
                    status=200)
            except Exception as e:
                if order:
                    order.delete()
                return HttpResponse(
                    content=f'Webhook received: {event["type"]} | ERROR: {e}',
                    status=500)
        # Send confirmation email if everything okay
        self._send_confirmation_email(order)
        return HttpResponse(
            content=(f'Webhook received: {event["type"]} | SUCCESS: '
                     'Created order in webhook'),
            status=200)

    def handle_payment_intent_payment_failed(self, event):
        """
        Handle the payment_intent.payment_failed webhook from Stripe
        """
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200)
