from django.test import TestCase
from django.shortcuts import reverse
from django.contrib.auth.models import User
from .models import GeneralEnquiry, Swarm


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
        init_record_count = len(GeneralEnquiry.objects.all())
        response = self.client.post(
            reverse('contact'),
            {
                'contact_name_full': 'Joe Test',
                'contact_email': 'joe@test.com',
                'contact_tel': '0123456789',
                'message_body': 'This is a test message'})
        self.assertRedirects(response, reverse('home'))
        end_record_count = len(GeneralEnquiry.objects.all())
        self.assertEqual(end_record_count, init_record_count + 1)

    def test_post_contact_success_authed(self):
        init_record_count = len(GeneralEnquiry.objects.all())
        self.user = User.objects.create_user(
            username='foobar',
            email='foo@bar.com',
            password='barbaz')
        self.client.force_login(user=self.user)
        response = self.client.post(
            reverse('contact'),
            {
                'contact_name_full': 'Joe Test',
                'contact_email': 'joe@test.com',
                'contact_tel': '0123456789',
                'message_body': 'This is a test message'})
        self.assertRedirects(response, reverse('home'))
        end_record_count = len(GeneralEnquiry.objects.all())
        self.assertEqual(end_record_count, init_record_count + 1)

    def test_post_contact_invalid(self):
        init_record_count = len(GeneralEnquiry.objects.all())
        self.user = User.objects.create_user(
            username='foobar',
            email='foo@bar.com',
            password='barbaz')
        self.client.force_login(user=self.user)
        response = self.client.post(
            reverse('contact'),
            {
                'contact_name_full': '',
                'contact_email': '',
                'contact_tel': '',
                'message_body': ''})
        self.assertTemplateUsed(response, 'contact/contact.html')
        end_record_count = len(GeneralEnquiry.objects.all())
        self.assertEqual(end_record_count, init_record_count)


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
        init_record_count = len(Swarm.objects.all())
        response = self.client.post(
            reverse('swarms'),
            {
                'contact_name_full': 'Joe Test',
                'contact_email': 'joe@test.com',
                'contact_tel': '0123456789',
                'message_body': 'This is a test message',
                'swarm_street_address1': '1 Test Street',
                'swarm_city': 'Testford',
                'swarm_country': 'GB'})
        self.assertRedirects(response, reverse('home'))
        end_record_count = len(Swarm.objects.all())
        self.assertEqual(end_record_count, init_record_count + 1)

    def test_post_swarms_success_authed(self):
        init_record_count = len(Swarm.objects.all())
        self.user = User.objects.create_user(
            username='foobar',
            email='foo@bar.com',
            password='barbaz')
        self.client.force_login(user=self.user)
        response = self.client.post(
            reverse('swarms'),
            {
                'contact_name_full': 'Joe Test',
                'contact_email': 'joe@test.com',
                'contact_tel': '0123456789',
                'message_body': 'This is a test message',
                'swarm_street_address1': '1 Test Street',
                'swarm_city': 'Testford',
                'swarm_country': 'GB'})
        self.assertRedirects(response, reverse('home'))
        end_record_count = len(Swarm.objects.all())
        self.assertEqual(end_record_count, init_record_count + 1)

    def test_post_swarms_invalid(self):
        init_record_count = len(Swarm.objects.all())
        self.user = User.objects.create_user(
            username='foobar',
            email='foo@bar.com',
            password='barbaz')
        self.client.force_login(user=self.user)
        response = self.client.post(
            reverse('swarms'),
            {
                'contact_name_full': '',
                'contact_email': '',
                'contact_tel': '',
                'message_body': ''})
        self.assertTemplateUsed(response, 'contact/swarms.html')
        end_record_count = len(Swarm.objects.all())
        self.assertEqual(end_record_count, init_record_count)
