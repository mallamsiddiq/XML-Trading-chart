from django.test import TestCase
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, logout
from . import User
class AuthAppTestCase(TestCase):

    def setUp(self):
        # Create a test user for authentication tests
        self.email = "TestUser@email.com"
        self.password = "5rXt9gQrfLZy7!6"
        self.user = User.objects.create_user(password=self.password, email = self.email)
        self.user2 = User.objects.create_user(password=self.password + '2', email = self.email + '2')

    def test_register_view(self):
        # Test registration view
        response = self.client.post(reverse_lazy('register'), {
            'password1': '5rXt9gQrfLZy7!6',
            'password2': '5rXt9gQrfLZy7!6',
            "email": "nmn@hj.com"
        })
        
        self.assertRedirects(response, reverse_lazy("home"))
        self.assertEqual(response.status_code, 302)  # Check for a successful redirect
        self.assertTrue(User.objects.filter(email='nmn@hj.com').exists())

    def test_registration_with_invalid_data(self):
        response = self.client.post(reverse_lazy('register'), {
            'email': 'invalid_email',  # Invalid email format
            'password1': 'password123',
            'password2': 'password456',  # Passwords do not match
        })
        self.assertEqual(response.status_code, 200)  # Check for a failed registration attempt
        self.assertFalse(User.objects.filter(email='invalid_email').exists())  # User should not be created

    def test_logout_when_not_logged_in(self):
        response = self.client.get(reverse_lazy('logout'))
        self.assertEqual(response.status_code, 302)  # Check for a redirect to login page or elsewhere
        # You can customize this based on your application's behavior


# Add more test cases as needed
