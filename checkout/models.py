import uuid

from django.db import models
from django.db.models import Sum
from django.conf import settings

from django_countries.fields import CountryField

from products.models import ProductStock
from profiles.models import UserProfile


class OrderStatus(models.Model):
    status_code = models.CharField(max_length=32)
    status_friendly = models.CharField(max_length=64, null=True, blank=True)

    def __str__(self):
        return self.status_code

    def get_friendly_name(self):
        return self.status_friendly


class Order(models.Model):
    order_number = models.CharField(max_length=32, null=False, editable=False)
    order_status = models.ForeignKey(OrderStatus, null=True, blank=True,
                                     on_delete=models.SET_NULL)
    user_profile = models.ForeignKey(UserProfile, on_delete=models.SET_NULL,
                                     null=True, blank=True,
                                     related_name='orders')
    order_date = models.DateTimeField(auto_now_add=True)
    name_full = models.CharField(max_length=50, null=False, blank=False)
    email = models.EmailField(max_length=254, null=False, blank=False)
    tel = models.CharField(max_length=20, null=False, blank=False)
    street_address1 = models.CharField(max_length=80, null=False, blank=False)
    street_address2 = models.CharField(max_length=80, null=True, blank=True)
    city = models.CharField(max_length=40, null=False, blank=False)
    county = models.CharField(max_length=80, null=True, blank=True)
    country = CountryField(blank_label='Country *', null=False, blank=False)
    postcode = models.CharField(max_length=20, null=True, blank=True)
    cost_delivery = models.DecimalField(max_digits=6, decimal_places=2,
                                        null=False, default=0)
    cost_total = models.DecimalField(max_digits=10, decimal_places=2,
                                     null=False, default=0)
    cost_grand_total = models.DecimalField(max_digits=10, decimal_places=2,
                                           null=False, default=0)
    original_bag = models.TextField(null=False, blank=False, default='')
    stripe_pid = models.CharField(max_length=254, null=False, blank=False,
                                  default='')

    def _generate_order_number(self):
        """
        Generate a random, unique order number using UUID
        """
        return uuid.uuid4().hex.upper()

    def update_total(self):
        """
        Update grand total each time a line item is added,
        accounting for delivery costs.
        """
        self.cost_total = self.lineitems.aggregate(
            Sum('lineitem_total'))['lineitem_total__sum'] or 0
        if self.cost_total < settings.FREE_DELIVERY_THRESHOLD:
            sdp = settings.STANDARD_DELIVERY_PERCENTAGE
            self.cost_delivery = self.cost_total * sdp / 100
        else:
            self.cost_delivery = 0
        self.cost_grand_total = self.cost_total + self.cost_delivery
        self.save()

    def save(self, *args, **kwargs):
        """
        Override the original save method to set the order number
        if it hasn't been set already.
        """
        if not self.order_number:
            self.order_number = self._generate_order_number()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.order_number


class OrderLineItem(models.Model):
    order = models.ForeignKey(Order, null=False, blank=False,
                              on_delete=models.CASCADE,
                              related_name='orderlineitems')
    product_line = models.ForeignKey(ProductStock, null=False, blank=False,
                                     on_delete=models.CASCADE)
    quantity = models.IntegerField(null=False, blank=False, default=0)
    lineitem_total = models.DecimalField(max_digits=6, decimal_places=2,
                                         null=False, blank=False,
                                         editable=False)

    def save(self, *args, **kwargs):
        """
        Override the original save method to set the lineitem total
        and update the order total.
        """
        self.lineitem_total = self.product_line.price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return (
            f'SKU {self.product_line.product.skup1}-{self.product_line.skup2}'
            f' on order {self.order.order_number}')
