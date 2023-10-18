from django.test import TestCase
from django.core.management import call_command
from authapp.models import Trader
from io import StringIO
import sys

class SeedTradersCommandTestCase(TestCase):

    def test_seed_traders_command_with_no_existing_traders(self):
        # Ensure there are no traders in the database before running the command
        self.assertEqual(Trader.objects.count(), 0)

        # Call the 'seed_traders' management command
        call_command('seed_traders')

        # Check if 10 traders have been created
        self.assertEqual(Trader.objects.count(), 10)

        # Check if each trader has an initial balance of $100
        for trader in Trader.objects.all():
            self.assertEqual(trader.balance, 100.0)

    def test_seed_traders_command_with_existing_traders(self):
        # Create some existing traders
        Trader.objects.create(email='existing1@gmail.com', balance=50.0)
        Trader.objects.create(email='existing2@gmail.com', balance=75.0)

        # Ensure there are existing traders in the database before running the command
        self.assertEqual(Trader.objects.count(), 2)

        # Call the 'seed_traders' management command
        call_command('seed_traders')

        # Check if the existing traders are not affected
        self.assertEqual(Trader.objects.count(), 2)

        # Check if the newly created traders have an initial balance of $100
        for trader in Trader.objects.exclude(email__in=['existing1@gmail.com', 'existing2@gmail.com']):
            self.assertEqual(trader.balance, 100.0)



    def test_seed_traders_command_with_existing_traders(self):
        # Create some existing traders
        Trader.objects.create(email='existing1@gmail.com', balance=50.0)
        Trader.objects.create(email='existing2@gmail.com', balance=75.0)

        # Ensure there are existing traders in the database before running the command
        self.assertEqual(Trader.objects.count(), 2)

        # Capture the standard output
        out = StringIO()
        sys.stdout = out

        # Call the 'seed_traders' management command
        call_command('seed_traders')

        # Reset standard output
        sys.stdout = sys.__stdout__

        # Check if the existing traders are not affected
        self.assertEqual(Trader.objects.count(), 2)

        # Check if the expected warning message is printed
        expected_output = "Traders already exist. Skipping seed.\n"
        self.assertEqual(out.getvalue(), expected_output)

        out.close()

        # Check if the newly created traders have an initial balance of $100
        for trader in Trader.objects.exclude(email__in=['existing1@gmail.com', 'existing2@gmail.com']):
            self.assertEqual(trader.balance, 100.0)
