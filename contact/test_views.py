from django.test import TestCase
from django.shortcuts import reverse
from django.contrib.auth.models import User
from .models import GeneralEnquiry, Swarm
from profiles.models import UserProfile


class TestViewsContact(TestCase):

    def test_get_contact_page_anom(self):
        response = self.client.get(reverse('contact'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'contact/contact.html')

    def test_get_contact_page_authed(self):
        self.user = User.objects.create_user(
            username='foobar',
            email='foo@bar.com',
            password='barbaz')
        self.client.force_login(user=self.user)
        response = self.client.get(reverse('contact'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'contact/contact.html')

    def test_post_contact_success_anom(self):
        response = self.client.post(
            reverse('contact'),
            {   'contact_name_full': 'Joe Test',
                'contact_email': 'joe@test.com',
                'contact_tel': '0123456789',
                'message_body': 'This is a test message'})
        self.assertRedirects(response, reverse('home'))
        records = GeneralEnquiry.objects.all()
        self.assertEqual(len(records), 1)

    def test_post_contact_success_authed(self):
        self.user = User.objects.create_user(
            username='foobar',
            email='foo@bar.com',
            password='barbaz')
        self.client.force_login(user=self.user)
        response = self.client.post(
            reverse('contact'),
            {   'contact_name_full': 'Joe Test',
                'contact_email': 'joe@test.com',
                'contact_tel': '0123456789',
                'message_body': 'This is a test message'})
        self.assertRedirects(response, reverse('home'))
        records = GeneralEnquiry.objects.all()
        self.assertEqual(len(records), 1)

    def test_post_contact_invalid(self):
        self.user = User.objects.create_user(
            username='foobar',
            email='foo@bar.com',
            password='barbaz')
        self.client.force_login(user=self.user)
        response = self.client.post(
            reverse('contact'),
            {   'contact_name_full': '',
                'contact_email': '',
                'contact_tel': '',
                'message_body': ''})
        self.assertTemplateUsed(response, 'contact/contact.html')
        records = GeneralEnquiry.objects.all()
        self.assertEqual(len(records), 0)

class TestViewsSwarms(TestCase):

    def test_get_swarms_page_anom(self):
        response = self.client.get(reverse('swarms'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'contact/swarms.html')

    def test_get_swarm_page_authed(self):
        self.user = User.objects.create_user(
            username='foobar',
            email='foo@bar.com',
            password='barbaz')
        self.client.force_login(user=self.user)
        response = self.client.get(reverse('swarms'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'contact/swarms.html')

    def test_post_swarms_success_anom(self):
        response = self.client.post(
            reverse('swarms'),
            {   'contact_name_full': 'Joe Test',
                'contact_email': 'joe@test.com',
                'contact_tel': '0123456789',
                'message_body': 'This is a test message',
                'swarm_street_address1': '1 Test Street',
                'swarm_city': 'Testford',
                'swarm_country': 'GB'})
        self.assertRedirects(response, reverse('home'))
        records = Swarm.objects.all()
        self.assertEqual(len(records), 1)

    def test_post_swarms_success_authed(self):
        self.user = User.objects.create_user(
            username='foobar',
            email='foo@bar.com',
            password='barbaz')
        self.client.force_login(user=self.user)
        response = self.client.post(
            reverse('swarms'),
            {   'contact_name_full': 'Joe Test',
                'contact_email': 'joe@test.com',
                'contact_tel': '0123456789',
                'message_body': 'This is a test message',
                'swarm_street_address1': '1 Test Street',
                'swarm_city': 'Testford',
                'swarm_country': 'GB'})
        self.assertRedirects(response, reverse('home'))
        records = Swarm.objects.all()
        self.assertEqual(len(records), 1)

    def test_post_swarms_invalid(self):
        self.user = User.objects.create_user(
            username='foobar',
            email='foo@bar.com',
            password='barbaz')
        self.client.force_login(user=self.user)
        response = self.client.post(
            reverse('swarms'),
            {   'contact_name_full': '',
                'contact_email': '',
                'contact_tel': '',
                'message_body': ''})
        self.assertTemplateUsed(response, 'contact/swarms.html')
        records = Swarm.objects.all()
        self.assertEqual(len(records), 0)
