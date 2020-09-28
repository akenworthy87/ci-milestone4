from django.test import TestCase
from .models import Category, ProductInfo, ProductStock


class TestModelsCategory(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name='test_cat',
            friendly_name='Test Category')

    def test_productinfo_string_method_returns_name(self):
        self.assertEqual(str(self.category), 'test_cat')

    def test_productinfo_string_method_returns_friendly(self):
        self.assertEqual(
            str(self.category.get_friendly_name()), 'Test Category')


class TestModelsProductInfo(TestCase):
    def setUp(self):
        self.product = ProductInfo.objects.create(
            name='Test Product',
            description='Test Product desc')

    def test_product_discontinued_defaults_to_false(self):
        self.assertFalse(self.product.product_discontinued)

    def test_productinfo_string_method_returns_name(self):
        self.assertEqual(str(self.product), 'Test Product')


class TestModelsProductStock(TestCase):
    def setUp(self):
        self.product = ProductInfo.objects.create(
            name='Test Product',
            description='Test Product desc')
        self.line1 = ProductStock.objects.create(
            product=self.product,
            variety_name='Test Line 1',
            price=6.66,
            stock_qty=100,
            stock_reserved=15)
        self.line2 = ProductStock.objects.create(
            product=self.product,
            variety_name='Test Line 2',
            price=6.66)

    def test_variety_discontinued_defaults_to_false(self):
        self.assertFalse(self.line1.variety_discontinued)

    def test_stock_qty_defaults_to_zero(self):
        self.assertEqual(int(self.line2.stock_qty), 0)

    def test_stock_reserved_defaults_to_zero(self):
        self.assertEqual(int(self.line2.stock_reserved), 0)

    def test_productinfo_string_method_returns_name(self):
        self.assertEqual(str(self.line1), 'Test Line 1')

    def test_productinfo_getstockavail_method_returns_stockavail(self):
        self.assertEqual(int(self.line1.get_stock_avail()), 85)

    def test_reserve_stock_quantity_greaterthan_stockavail(self):
        with self.assertRaises(ValueError):
            self.line1.reserve_stock(100, True)

    def test_reserve_stock_quantity_lessthan_stockavail_dry(self):
        self.assertIsNone(self.line1.reserve_stock(50, True))
        self.assertEqual(int(self.line1.stock_reserved), 15)

    def test_reserve_stock_quantity_lessthan_stockavail_wet(self):
        self.assertIsNone(self.line1.reserve_stock(50))
        self.assertEqual(int(self.line1.stock_reserved), 65)
