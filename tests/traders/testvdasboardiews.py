from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from traders.models import Transaction  # Import your Trader model
from authapp.models import Trader
from django.contrib.messages import get_messages
from datetime import datetime
from decimal import Decimal

import json


User = get_user_model()

from django.template.defaultfilters import date as date_filter

class DashboardViewTest(TestCase):
    def setUp(self):
        # Create a test user
        self.trader = self.user = Trader.objects.create_user(email='testuser', password='testpassword')

    def test_dashboard_view_as_trader(self):
        # Log in the user
        self.client.login(email='testuser', password='testpassword')

        # Access the view
        response = self.client.get(reverse('dashboard'))

        # Check if the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Add more specific assertions to test the view's behavior when accessed by a trader

    def test_dashboard_view_as_non_trader(self):
        # Create a test user who is not a trader (e.g., a regular user)
        non_trader_user = User.objects.create_user(email='nontrader', password='testpassword')

        # Log in the non-trader user
        self.client.login(email='nontrader', password='testpassword')

        # Access the view
        response = self.client.get(reverse('dashboard'))
        
        # Assert that the response redirects to the expected URL (e.g., 'home')
        self.assertRedirects(response, reverse('home'))

        # Check if a message is set in the response indicating the reason for the redirect
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(messages)  # Check if there are messages
        expected_message = "You have no transactions, Consider Trading"
        self.assertIn(expected_message, [str(message) for message in messages])

    def test_dashboard_view_as_a_no_user(self):
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login') + '?next=/dashboard')



    def test_dashboard_view_with_date_filter(self):
        # Log in the user
        self.client.login(email='testuser', password='testpassword')

        # Create transactions with different dates
        number_of_transactions = 1000
        for idx in range(number_of_transactions):
            # Create and associate transactions with the trader
            date = datetime(2023, 1, 1) if idx % 2 == 0 else datetime(2023, 2, 1)
            transaction = Transaction(
                customer=self.trader,
                description=f"some {idx} transaction",
                amount=Decimal('10.00') * (idx % 5),
                created_date = date
            )
            transaction.save()

        # Access the view with a specific date range
        start_date = '2023-01-01'
        end_date = '2023-02-01'
        response = self.client.get(reverse('dashboard') + f'?start={start_date}&end={end_date}')

        # Check if the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Get the transactions from the context
        transactions = response.context['transactions']

        # Check if the transactions are correctly filtered within the date range
        for transaction in transactions:
            self.assertTrue(start_date <= transaction.created_date <= end_date)

    def test_dashboard_view_data_lists(self):
        # Log in the user
        self.client.login(email='testuser', password='testpassword')

        # Create transactions with different data
        transactions = []
        for idx in range(10):
            date = datetime(2023, 1, 1)
            amount = Decimal('10.00') * (idx % 5)
            balance = Decimal('1000.00') + amount * (idx % 2)
            transaction = Transaction(
                customer=self.trader,
                description=f"some {idx} transaction",
                amount=amount,
                created_date=date,
                balance=balance
            )
            transaction.save()
            transactions.append(transaction)

        # Access the view
        response = self.client.get(reverse('dashboard'))

        # Check if the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Get the lists from the context
        timestamps = timestamps = json.loads(response.context['data_labels'])
        profit_loss = response.context['data_values']
        prev_balance = response.context['prev_balance']
        bar_data = response.context['bar_data']

        # Check if the generated lists match the expected values
        expected_timestamps = [date_filter(transaction.created_date, "c") for transaction in transactions]
        expected_profit_loss = [transaction.balance for transaction in transactions]
        expected_prev_balance = [
            (transaction.balance - transaction.amount, transaction.balance)[transaction.amount < 0 and transaction.balance - transaction.amount > 0]
            for transaction in transactions
        ]
        expected_bar_data = [(
            transaction.amount,
            abs(transaction.amount)
        )[(transaction.balance - transaction.amount) > 0] for transaction in transactions]

        self.assertEqual(timestamps, expected_timestamps)
        self.assertEqual(profit_loss, expected_profit_loss)
        self.assertEqual(prev_balance, expected_prev_balance)
        self.assertEqual(bar_data, expected_bar_data)