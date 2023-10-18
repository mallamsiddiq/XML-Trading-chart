from django.core.management import call_command
from django.test import TestCase
from django.contrib.auth import get_user_model
from io import StringIO

User = get_user_model()

class MakeAdminCommandTestCase(TestCase):
    def test_make_admin_command_no_existing_admin(self):
        # Ensure no admin user exists in the database
        self.assertFalse(User.objects.filter(is_superuser=True).exists())

        # Capture the command's output for testing
        out = StringIO()
        call_command('makeadmin', stdout=out)

        output = out.getvalue()

        # Check if the command printed a success message
        self.assertIn('Successfully created admin:', output)
        # Check if the admin user was actually created
        self.assertTrue(User.objects.filter(email='admin@ftnja.com', is_superuser=True, is_staff=True).exists())

    def test_make_admin_command_existing_admin(self):
        # Create an existing admin user
        User.objects.create_superuser(email='admin@ftnja.com', password='admin')

        # Capture the command's output for testing
        out = StringIO()
        call_command('makeadmin', stdout=out)

        output = out.getvalue()

        # Check if the command printed a warning message
        self.assertIn('An admin user already exists in the database', output)
        # Check that no new admin user was created
        self.assertEqual(User.objects.filter(email='admin@ftnja.com').count(), 1)
