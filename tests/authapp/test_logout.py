from django.test import TestCase
from . import User
from unittest.mock import patch


from django.urls import reverse_lazy

class CustomLogoutViewTest(TestCase):

    def setUp(self):
        self.payload = {
            'email' : "TestUser@email.com",
            'password' : "5rXt9gQrfLZy7!6"
        }
        self.user = User.objects.create_user(**self.payload)

        self.logout_url = reverse_lazy('logout')

    def test_logout(self):
        # Log in the user
        login_successful = self.client.login(**self.payload)
        self.assertTrue(login_successful)  # Check if login was successful

        # Make a GET request to your custom logout view
        response = self.client.get(self.logout_url)  # Replace with the actual URL of your custom logout view

        self.assertRedirects(response, reverse_lazy('login'))  # Replace 'login' with your actual login page URL name
        self.assertFalse(response.wsgi_request.user.is_authenticated)
        self.assertIsNone(response.wsgi_request.session.get('_auth_user_id'))

    def test_logout_without_loggedin(self):
        # Log in the user

        # Make a GET request to your custom logout view
        response = self.client.get(self.logout_url)  # Replace with the actual URL of your custom logout view

        self.assertRedirects(response, f"{reverse_lazy('login')}?next={reverse_lazy('logout')}")  # Replace 'login' with your actual login page URL name
        self.assertFalse(response.wsgi_request.user.is_authenticated)
        self.assertIsNone(response.wsgi_request.session.get('_auth_user_id'))