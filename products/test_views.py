from django.test import TestCase
from django.shortcuts import reverse
from django.contrib.auth.models import User
from .models import ProductInfo, ProductStock


class TestViews(TestCase):
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

    def test_get_product_list(self):
        response = self.client.get(reverse('products'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/products.html')

    def test_product_detail(self):
        response = self.client.get(
            reverse('product_detail', args=[self.product.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/product_detail.html')

    def test_product_detail_discontinued(self):
        self.product.product_discontinued = True
        self.product.save()
        response = self.client.get(
            reverse('product_detail', args=[self.product.id]),
            follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse('home'))


class TestDiscontinueProduct(TestCase):
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

    def test_discontinue_product(self):
        self.assertFalse(
            self.product.product_discontinued,
            "Product already discontinued")
        self.user = User.objects.create_superuser(
            username='foobar',
            email='foo@bar.com',
            password='barbaz')
        self.client.force_login(user=self.user)
        response = self.client.get(
            reverse('discontinue_product', args=[self.product.id]),
            follow=True)
        updated_item = ProductInfo.objects.get(id=self.product.id)
        self.assertTrue(updated_item.product_discontinued)
        self.assertRedirects(response, reverse('products'))

    def test_discontinue_product_normaluser_gohome(self):
        self.assertFalse(
            self.product.product_discontinued,
            "Product already discontinued")
        self.user = User.objects.create_user(
            username='foobar',
            email='foo@bar.com',
            password='barbaz')
        self.client.force_login(user=self.user)
        response = self.client.get(
            reverse('discontinue_product', args=[self.product.id]),
            follow=True)
        updated_item = ProductInfo.objects.get(id=self.product.id)
        self.assertFalse(updated_item.product_discontinued)
        self.assertRedirects(response, reverse('home'))

    def test_discontinue_product_loggedout_redir_login(self):
        response = self.client.get(
            reverse('discontinue_product', args=[self.product.id]),
            follow=True)
        updated_item = ProductInfo.objects.get(id=self.product.id)
        self.assertFalse(updated_item.product_discontinued)
        self.assertRedirects(
            response,
            f'/accounts/login/?next=/products/discontinue/{self.product.id}/')


class TestDiscontinueProductLine(TestCase):
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

    def test_discontinue_product_line(self):
        self.assertFalse(
            self.line1.variety_discontinued,
            "Product line already discontinued")
        self.user = User.objects.create_superuser(
            username='foobar',
            email='foo@bar.com',
            password='barbaz')
        self.client.force_login(user=self.user)
        response = self.client.get(
            reverse('discontinue_line', args=[self.line1.id]),
            follow=True)
        updated_item = ProductStock.objects.get(id=self.line1.id)
        self.assertTrue(updated_item.variety_discontinued)
        self.assertRedirects(response, reverse('products'))

    def test_discontinue_product_line_normaluser_gohome(self):
        self.assertFalse(
            self.line1.variety_discontinued,
            "Product already discontinued")
        self.user = User.objects.create_user(
            username='foobar',
            email='foo@bar.com',
            password='barbaz')
        self.client.force_login(user=self.user)
        response = self.client.get(
            reverse('discontinue_line', args=[self.line1.id]),
            follow=True)
        updated_item = ProductStock.objects.get(id=self.line1.id)
        self.assertFalse(updated_item.variety_discontinued)
        self.assertRedirects(response, reverse('home'))

    def test_discontinue_product_line_loggedout_redir_login(self):
        response = self.client.get(
            reverse('discontinue_line', args=[self.line1.id]),
            follow=True)
        updated_item = ProductStock.objects.get(id=self.line1.id)
        self.assertFalse(updated_item.variety_discontinued)
        self.assertRedirects(
            response,
            f'/accounts/login/?next=/products/discontinue_line/{self.product.id}/')


class TestDeleteProduct(TestCase):
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

    def test_delete_product(self):
        self.user = User.objects.create_superuser(
            username='foobar',
            email='foo@bar.com',
            password='barbaz')
        self.client.force_login(user=self.user)
        response = self.client.get(
            reverse('delete_product', args=[self.product.id]),
            follow=True)
        existing_items = ProductInfo.objects.filter(id=self.product.id)
        self.assertEqual(len(existing_items), 0, "Item wasn't deleted!")
        self.assertRedirects(response, reverse('products'))

    def test_delete_product_normaluser_gohome(self):
        self.user = User.objects.create_user(
            username='foobar',
            email='foo@bar.com',
            password='barbaz')
        self.client.force_login(user=self.user)
        response = self.client.get(
            reverse('delete_product', args=[self.product.id]),
            follow=True)
        existing_items = ProductInfo.objects.filter(id=self.product.id)
        self.assertEqual(len(existing_items), 1)
        self.assertRedirects(response, reverse('home'))

    def test_delete_product_loggedout_redir_login(self):
        response = self.client.get(
            reverse('delete_product', args=[self.product.id]),
            follow=True)
        existing_items = ProductInfo.objects.filter(id=self.product.id)
        self.assertEqual(len(existing_items), 1)
        self.assertRedirects(
            response,
            f'/accounts/login/?next=/products/delete/{self.product.id}/')


class TestRedirectProductManagement(TestCase):

    def test_management_redirect_requires_loggon(self):
        response = self.client.get(reverse('product_management'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(
            response,
            '/accounts/login/?next=/products/management/')

    def test_management_redirect_normaluser_reject(self):
        self.user = User.objects.create_user(
            username='foobar',
            email='foo@bar.com',
            password='barbaz')
        self.client.force_login(user=self.user)
        response = self.client.get(reverse('product_management'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(
            response,
            '/admin/login/?next=/admin/products/')

    def test_management_redirect_superuser_pass(self):
        self.user = User.objects.create_superuser(
            username='foobar',
            email='foo@bar.com',
            password='barbaz')
        self.client.force_login(user=self.user)
        response = self.client.get(reverse('product_management'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(
            response,
            '/admin/products/')


class TestRedirectAddProduct(TestCase):

    def test_add_product_redirect_requires_loggon(self):
        response = self.client.get(reverse('add_product'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(
            response,
            '/accounts/login/?next=/products/add/')

    def test_add_product_redirect_normaluser_reject(self):
        self.user = User.objects.create_user(
            username='foobar',
            email='foo@bar.com',
            password='barbaz')
        self.client.force_login(user=self.user)
        response = self.client.get(reverse('add_product'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(
            response,
            '/admin/login/?next=/admin/products/productinfo/add/')

    def test_add_product_redirect_superuser_pass(self):
        self.user = User.objects.create_superuser(
            username='foobar',
            email='foo@bar.com',
            password='barbaz')
        self.client.force_login(user=self.user)
        response = self.client.get(reverse('add_product'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(
            response,
            '/admin/products/productinfo/add/')


class TestRedirectEditProduct(TestCase):
    def setUp(self):
        self.product = ProductInfo.objects.create(
            name='Test Product',
            description='Test Product desc')

    def test_edit_product_redirect_requires_loggon(self):
        response = self.client.get(
            reverse('edit_product', args=[self.product.id]),
            follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(
            response,
            f'/accounts/login/?next=/products/edit/{self.product.id}/')

    def test_edit_product_redirect_normaluser_reject(self):
        self.user = User.objects.create_user(
            username='foobar',
            email='foo@bar.com',
            password='barbaz')
        self.client.force_login(user=self.user)
        response = self.client.get(
            reverse('edit_product', args=[self.product.id]),
            follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(
            response,
            f'/admin/login/?next=/admin/products/productinfo/{self.product.id}/change/')

    def test_edit_product_redirect_superuser_pass(self):
        self.user = User.objects.create_superuser(
            username='foobar',
            email='foo@bar.com',
            password='barbaz')
        self.client.force_login(user=self.user)
        response = self.client.get(
            reverse('edit_product', args=[self.product.id]),
            follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(
            response,
            f'/admin/products/productinfo/{self.product.id}/change/')
