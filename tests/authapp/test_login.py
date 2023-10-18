from django.test import TestCase
from django.urls import reverse_lazy
from . import User
from django.contrib.messages import get_messages
from authapp.forms import BaseLoginForm  # Import your custom login form

class LoginViewTestCase(TestCase):
    def setUp(self):
        # Create a test user
        self.email = "TestUser@email.com"
        self.password = "5rXt9gQrfLZy7!6"

        self.login_url = reverse_lazy('login')
        
        self.user = User.objects.create_user(
            password = self.password,
            email = self.email
        )


        self.payload = {
            'email': self.email,  # Use 'email' as the field name for email
            'password': self.password,
        }

    def test_login_view(self):
        # Get the login page
        response = self.client.get(self.login_url)

        # Check that the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Check that the correct template is used
        self.assertTemplateUsed(response, 'authapp/login.html')

        # Check that the login form is an instance of your custom BaseLoginForm
        self.assertIsInstance(response.context['form'], BaseLoginForm)

        # Attempt to log in with valid credentials
        # login_data = 

        response = self.client.post(self.login_url, self.payload)

        # Check that the user is redirected to the 'home' page after login
        self.assertRedirects(response, reverse_lazy('home'))

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), f"You have been successfully logged in as {self.email}")

        # Check that the user is now authenticated
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_login_with_invalid_credentials(self):
        # Attempt to log in with invalid credentials

        self.payload = {
            'email' : self.email,
            'password': '1234',
        }

        response = self.client.post(self.login_url, self.payload, follow=True)



        # Check that the user remains on the login page
        self.assertTemplateUsed(response, 'authapp/login.html')
        # Check if the "Invalid login credentials" error message is present
        self.assertFormError(response, 'form', None, 'Invalid login credentials')

        # Check that an error message is displayed
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Invalid username or password')
