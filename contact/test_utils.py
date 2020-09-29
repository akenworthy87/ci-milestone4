from django.test import TestCase
from unittest.mock import MagicMock
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from .models import GeneralEnquiry, Swarm
from .forms import GeneralEnquiryForm, SwarmForm
from .utils import (post_actions,
                    send_message_confirmation_email,
                    send_swarms_list_email)


class TestPostActionsGeneralEnq(TestCase):

    def test_valid_form_anom(self):
        post_data = {
            'contact_name_full': 'Joe Test',
            'contact_email': 'joe@test.com',
            'contact_tel': '0123456789',
            'message_body': 'This is a test message'}
        request = MagicMock()
        request.user = AnonymousUser()
        form = GeneralEnquiryForm(post_data)
        enquiry = post_actions(request, form)
        self.assertIsInstance(enquiry, GeneralEnquiry)
        self.assertTrue(enquiry.id)
        self.assertEqual(enquiry.message_body, 'This is a test message')
        self.assertFalse(enquiry.user_profile)

    def test_valid_form_authed(self):
        post_data = {
            'contact_name_full': 'Joe Test',
            'contact_email': 'joe@test.com',
            'contact_tel': '0123456789',
            'message_body': 'This is a test message'}
        request = MagicMock()
        request.user = User.objects.create_user(
            username='foobar',
            email='foo@bar.com',
            password='barbaz')
        form = GeneralEnquiryForm(post_data)
        enquiry = post_actions(request, form)
        self.assertIsInstance(enquiry, GeneralEnquiry)
        self.assertTrue(enquiry.id)
        self.assertEqual(enquiry.message_body, 'This is a test message')
        self.assertEqual(str(enquiry.user_profile), 'foobar')

    def test_invalid_form_anom(self):
        post_data = {
            'contact_name_full': '',
            'contact_email': '',
            'contact_tel': '',
            'message_body': ''}
        request = MagicMock()
        request.user = AnonymousUser()
        form = GeneralEnquiryForm(post_data)
        enquiry = post_actions(request, form)
        self.assertFalse(enquiry)


class TestPostActionsSwarms(TestCase):

    def test_valid_form_anom(self):
        post_data = {
            'contact_name_full': 'Joe Test',
            'contact_email': 'joe@test.com',
            'contact_tel': '0123456789',
            'message_body': 'This is a test message',
            'swarm_street_address1': '1 Test Street',
            'swarm_city': 'Testford',
            'swarm_country': 'GB'}
        request = MagicMock()
        request.user = AnonymousUser()
        form = SwarmForm(post_data)
        enquiry = post_actions(request, form)
        self.assertIsInstance(enquiry, Swarm)
        self.assertTrue(enquiry.id)
        self.assertEqual(enquiry.message_body, 'This is a test message')
        self.assertFalse(enquiry.user_profile)

    def test_valid_form_authed(self):
        post_data = {
            'contact_name_full': 'Joe Test',
            'contact_email': 'joe@test.com',
            'contact_tel': '0123456789',
            'message_body': 'This is a test message',
            'swarm_street_address1': '1 Test Street',
            'swarm_city': 'Testford',
            'swarm_country': 'GB'}
        request = MagicMock()
        request.user = User.objects.create_user(
            username='foobar',
            email='foo@bar.com',
            password='barbaz')
        form = SwarmForm(post_data)
        enquiry = post_actions(request, form)
        self.assertIsInstance(enquiry, Swarm)
        self.assertTrue(enquiry.id)
        self.assertEqual(enquiry.message_body, 'This is a test message')
        self.assertEqual(str(enquiry.user_profile), 'foobar')

    def test_invalid_form_anom(self):
        post_data = {
            'contact_name_full': '',
            'contact_email': '',
            'contact_tel': '',
            'message_body': ''}
        request = MagicMock()
        request.user = AnonymousUser()
        form = SwarmForm(post_data)
        enquiry = post_actions(request, form)
        self.assertFalse(enquiry)


class TestConfirmationEmails(TestCase):
    def setUp(self):
        data = {
            'contact_name_full': 'Joe Test',
            'contact_email': 'joe@test.com',
            'contact_tel': '0123456789',
            'message_body': 'This is a test message',
            'swarm_street_address1': '1 Test Street',
            'swarm_city': 'Testford',
            'swarm_country': 'GB'}
        self.message = Swarm.objects.create(**data)

    def test_send_message_confirmation_email(self):
        result = send_message_confirmation_email(self.message, 'TEST')
        self.assertIsNone(result)

    def test_template_subject(self):
        subject = render_to_string(
            'contact/confirmation_emails/confirmation_email_subject.txt',
            {'message': self.message, 'ref': 'TEST'})
        self.assertEqual(
            subject,
            'Stonecroft Bees Message Confirmation - TEST: 1')

    def test_template_body(self):
        body = render_to_string(
            'contact/confirmation_emails/confirmation_email_body.txt',
            {'message': self.message, 'contact_email': 'from@test.com'})
        self.assertIn(self.message.contact_name_full, body)
        self.assertIn(self.message.contact_tel, body)
        self.assertIn(self.message.contact_email, body)
        self.assertIn(self.message.message_body, body)
        self.assertIn('from@test.com', body)


class TestSwarmEmails(TestCase):
    def setUp(self):
        data = {
            'contact_name_full': 'Joe Test',
            'contact_email': 'joe@test.com',
            'contact_tel': '0123456789',
            'message_body': 'This is a test message',
            'swarm_street_address1': '1 Test Street',
            'swarm_street_address2': 'West Teston',
            'swarm_city': 'Testford',
            'swarm_county': 'West Testshire',
            'swarm_country': 'GB',
            'swarm_postcode': 'TE5 7ER'}
        self.message = Swarm.objects.create(**data)

    def test_send_message_confirmation_email(self):
        result = send_swarms_list_email(self.message, 'SWMTEST')
        self.assertIsNone(result)

    def test_template_subject(self):
        subject = render_to_string(
            'contact/swarm_emails/new_swarm_subject.txt',
            {'message': self.message, 'ref': 'SWMTEST'})
        self.assertEqual(
            subject,
            'Stonecroft Bees - New Swarm Reported - SWMTEST: 1')

    def test_template_body(self):
        body = render_to_string(
            'contact/swarm_emails/new_swarm_body.txt',
            {'message': self.message, 'contact_email': 'from@test.com'})
        self.assertIn(self.message.contact_name_full, body)
        self.assertIn(self.message.contact_tel, body)
        self.assertIn(self.message.contact_email, body)
        self.assertIn(self.message.message_body, body)
        self.assertIn(self.message.swarm_street_address1, body)
        self.assertIn(self.message.swarm_street_address2, body)
        self.assertIn(self.message.swarm_city, body)
        self.assertIn(self.message.swarm_county, body)
        self.assertIn(str(self.message.swarm_country), body)
        self.assertIn(self.message.swarm_postcode, body)
        self.assertIn('from@test.com', body)
