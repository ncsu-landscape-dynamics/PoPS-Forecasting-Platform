from django.test import TestCase
from django.urls import reverse

class LandingPageViewTest(TestCase):

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)
           
    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('landing_page'))
        self.assertEqual(response.status_code, 200)

class FAQPageViewTest(TestCase):

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/faq/')
        self.assertEqual(response.status_code, 200)
           
    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('FAQs'))
        self.assertEqual(response.status_code, 200)

class TutorialsPageViewTest(TestCase):

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/tutorials/')
        self.assertEqual(response.status_code, 200)
           
    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('tutorials'))
        self.assertEqual(response.status_code, 200)
        
class TermsAndConditionsPageViewTest(TestCase):

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/terms_and_conditions/')
        self.assertEqual(response.status_code, 200)
           
    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('terms_and_conditions'))
        self.assertEqual(response.status_code, 200)
 
class PrivacyPolicyPageViewTest(TestCase):

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/privacy_policy/')
        self.assertEqual(response.status_code, 200)
           
    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('privacy_policy'))
        self.assertEqual(response.status_code, 200)