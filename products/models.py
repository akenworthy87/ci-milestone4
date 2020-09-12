from django.db import models


class Category(models.Model):

    class Meta:
        verbose_name_plural = 'Categories'

    name = models.CharField(max_length=32)
    friendly_name = models.CharField(max_length=64, null=True, blank=True)

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        return self.friendly_name


class ProductInfo(models.Model):
    category = models.ForeignKey('Category', null=True, blank=True,
                                 on_delete=models.SET_NULL)
    name = models.CharField(max_length=254)
    description = models.TextField()
    skup1 = models.CharField(max_length=254, null=True, blank=True)
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    rating = models.DecimalField(max_digits=6, decimal_places=2, null=True,
                                 blank=True)
    product_discontinued = models.BooleanField(default=False,
                                               null=True, blank=True)

    def __str__(self):
        return self.name


class ProductStock(models.Model):
    product = models.ForeignKey('ProductInfo', null=True, blank=True,
                                on_delete=models.SET_NULL,
                                related_name='productlines')
    skup2 = models.CharField(max_length=254, null=True, blank=True)
    variety_name = models.CharField(max_length=254)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    stock_qty = models.IntegerField(default=0)
    stock_reserved = models.IntegerField(default=0)
    variety_discontinued = models.BooleanField(default=False, null=True,
                                               blank=True)

    def __str__(self):
        return self.variety_name

    def get_stock_avail(self):
        """ Returns the availible stock quantity """
        return self.stock_qty - self.stock_reserved

    def reserve_stock(self, quantity):
        """
        Attempts to reserve stock by specified quantity.
        First checks quantity is availible, raises ValueError if not.
        Then increments current reserved stock level by specified quantity.
        """
        if quantity > self.get_stock_avail():
            raise ValueError(
                f"Requested quantity({quantity}) is higher "
                f"than availible({self.get_stock_avail()}) "
                f"for {self.variety_name} - {self.product.name}")
        else:
            self.stock_reserved += quantity
            self.save()
