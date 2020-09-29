from django.test import TestCase
from .forms import GeneralEnquiryForm, SwarmForm


class TestGeneralEnquiryForm(TestCase):

    def test_valid_form(self):
        form_data = {
            'contact_name_full': 'Joe Test',
            'contact_email': 'joe@test.com',
            'contact_tel': '0123456789',
            'message_body': 'This is a test message'}
        form = GeneralEnquiryForm(form_data)
        self.assertTrue(form.is_valid())

    def test_fields_are_explicit_in_form_metaclass(self):
        form = GeneralEnquiryForm()
        self.assertEqual(
            form.Meta.fields,
            ('contact_name_full', 'contact_email',
             'contact_tel', 'message_body'))

    def test_required_fields(self):
        form = GeneralEnquiryForm({'contact_name_full': ''})
        self.assertFalse(form.is_valid())
        required_fields = (
            'contact_name_full', 'contact_email',
            'contact_tel', 'message_body')
        # Self test to check the test is checking the right number of fields
        self.assertEqual(
            len(required_fields),
            len(form.errors),
            "Required Fields not equal to Form Errors.")
        for field in required_fields:
            self.assertIn(field, form.errors.keys())
            self.assertEqual(form.errors[field][0], 'This field is required.')


class TestSwarmForm(TestCase):

    def test_valid_form(self):
        form_data = {
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
        form = SwarmForm(form_data)
        self.assertTrue(form.is_valid())

    def test_fields_are_explicit_in_form_metaclass(self):
        form = SwarmForm()
        self.assertEqual(
            form.Meta.fields,
            ('contact_name_full', 'contact_email', 'contact_tel',
             'swarm_street_address1', 'swarm_street_address2',
             'swarm_city', 'swarm_county', 'swarm_country',
             'swarm_postcode', 'message_body'))

    def test_required_fields(self):
        form = SwarmForm({'contact_name_full': ''})
        self.assertFalse(form.is_valid())
        required_fields = (
            'contact_name_full', 'contact_email',
            'contact_tel', 'message_body',
            'swarm_street_address1', 'swarm_city',
            'swarm_country')
        # Self test to check the test is checking the right number of fields
        self.assertEqual(
            len(required_fields),
            len(form.errors),
            "Required Fields not equal to Form Errors.")
        for field in required_fields:
            self.assertIn(field, form.errors.keys())
            self.assertEqual(form.errors[field][0], 'This field is required.')
