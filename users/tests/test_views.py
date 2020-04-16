from django.test import TestCase, SimpleTestCase
from django.urls import reverse
from django.http import HttpRequest
from django.conf import settings
from users.models import CustomUser

# Create your tests here.
class LoginPageTests(SimpleTestCase):

    def test_login_page_status_code(self):
        response = self.client.get('/accounts/login/')
        self.assertEquals(response.status_code, 200)

    def test_view_url_by_name(self):
        response = self.client.get(reverse('login'))
        self.assertEquals(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('login'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/login.html')

    def test_login_page_contains_correct_html(self):
        response = self.client.get('/accounts/login/')
        self.assertContains(response, 'Log in')

    def test_home_page_does_not_contain_incorrect_html(self):
        response = self.client.get('/accounts/login/')
        self.assertNotContains(
            response, 'Hi there! I should not be on the page.')

    def test_login_redirect(self):
        response = self.client.get('/workspace/')
        self.assertRedirects(response, '/accounts/login/?next=/workspace/')

class SignUpPageTests(SimpleTestCase):

    def test_page_status_code(self):
        response = self.client.get('/accounts/signup/')
        self.assertEquals(response.status_code, 200)

    def test_view_url_by_name(self):
        response = self.client.get(reverse('signup'))
        self.assertEquals(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('signup'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'signup.html')

    def test_login_page_contains_correct_html(self):
        response = self.client.get('/accounts/signup/')
        self.assertContains(response, 'Sign up')

    def test_home_page_does_not_contain_incorrect_html(self):
        response = self.client.get('/accounts/signup/')
        self.assertNotContains(
            response, 'Hi there! I should not be on the page.')

class AccountActivationEmailSentPageTests(SimpleTestCase):

    def test_login_page_status_code(self):
        response = self.client.get('/accounts/account_activation_sent/')
        self.assertEquals(response.status_code, 200)

    def test_view_url_by_name(self):
        response = self.client.get(reverse('account_activation_sent'))
        self.assertEquals(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('account_activation_sent'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'account_activation_sent.html')

    def test_login_page_contains_correct_html(self):
        response = self.client.get('/accounts/account_activation_sent/')
        self.assertContains(response, 'Email sent')

    def test_home_page_does_not_contain_incorrect_html(self):
        response = self.client.get('/accounts/account_activation_sent/')
        self.assertNotContains(
            response, 'Hi there! I should not be on the page.')

class MyAccountTests(TestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(username='test', first_name='test_first', last_name='test_last',
                                              email='testuser@test.com', user_type='OTHER', password='testpass')
        self.client.force_login(self.user)

    def test_user(self):
        self.assertEqual(self.user.username, 'test')

    def test_account_page_status_code(self):
        response = self.client.get('/accounts/my_account/')
        self.assertEquals(response.status_code, 200)

    def test_view_url_by_name(self):
        response = self.client.get(reverse('my_account'))
        self.assertEquals(response.status_code, 200)

class UserTest(TestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(username='test', first_name='test_first', last_name='test_last',
                                              email='testuser@test.com', user_type='OTHER', password='testpass')
        self.client.force_login(self.user)

    def test_user(self):
        self.assertEqual(self.user.username, 'test')

    def test_account_status_code(self):
        response = self.client.get('/accounts/my_account/')
        self.assertEquals(response.status_code, 200)

    def test_account_view_url_by_name(self):
        response = self.client.get(reverse('my_account'))
        self.assertEquals(response.status_code, 200)

    def test_update_status_code(self):
        response = self.client.get('/accounts/update/')
        self.assertEquals(response.status_code, 200)

    def test_update_view_url_by_name(self):
        response = self.client.get(reverse('update_account'))
        self.assertEquals(response.status_code, 200)

    def test_workspace_status_code(self):
        response = self.client.get('/workspace/')
        self.assertEquals(response.status_code, 200)

    def test_workspace_url_by_name(self):
        response = self.client.get(reverse('workspace'))
        self.assertEquals(response.status_code, 200)

    def test_login_page_contains_correct_html(self):
        response = self.client.get(reverse('workspace'))
        self.assertContains(response, 'Welcome')
        self.assertContains(response, 'test')

