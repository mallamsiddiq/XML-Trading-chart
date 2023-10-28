from django.core.management import call_command
from django.test import TestCase
from authapp.models import Trader
from django.contrib.auth import get_user_model

User = get_user_model()


class SimulateTransactionsCommandTestCase(TestCase):

    def setUp(self):
        # Create traders for testing
        self.trader1 = Trader.objects.create(email='testuser1', balance=100.0)
        self.trader2 = Trader.objects.create(email='testuser2', balance=200.0)

    def test_simulate_transactions_command(self):
        # Store initial balances
        trader1_early_balance = self.trader1.balance
        trader2_early_balance = self.trader2.balance

        num_transactions = 5  # Provide the desired value for num_transactions (optional)
        delay = 15

        call_command('simulate_profit_loss', f'--num_transactions={num_transactions}', f'--delay={delay}')

        # Refresh trader instances from the database to get updated balances
        self.trader1.refresh_from_db()
        self.trader2.refresh_from_db()

        # Check if transactions have been created for each trader
        self.assertEqual(self.trader1.transactions.count(), num_transactions)  # Assuming num_transactions minutes
        self.assertEqual(self.trader2.transactions.count(), num_transactions)

        # Calculate the expected balances based on simulated transactions
        for i in range(1, num_transactions + 1):
            random_transaction = self.trader1.transactions.filter(
                description__icontains=f"@ {i} Minute"
            ).first()
            if random_transaction:
                trader1_early_balance += random_transaction.amount

        for i in range(1, num_transactions + 1):
            random_transaction = self.trader2.transactions.filter(
                description__icontains=f"@ {i} Minute"
            ).first()
            if random_transaction:
                trader2_early_balance += random_transaction.amount

        # Check if the balances match the expected values
        self.assertEqual(self.trader1.balance, trader1_early_balance)
        self.assertEqual(self.trader2.balance, trader2_early_balance)
