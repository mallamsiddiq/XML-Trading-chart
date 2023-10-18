import datetime
from django.test import TestCase
from django.contrib.auth import get_user_model
from authapp.models import Trader
from traders.models import Transaction, Credit, Debit, Report, NoNegativeError

class TransactionModelTestCase(TestCase):

    def setUp(self):
        # self.user = get_user_model().objects.create(email='testuser')
        self.trader = Trader.objects.create(email='testuser', balance = 50)

    def test_transaction_creation(self):
        transaction = Transaction.objects.create(
            customer=self.trader,
            description='Test Transaction',
            amount=50.0
        )
        self.assertEqual(transaction.customer, self.trader)
        self.assertEqual(transaction.description, 'Test Transaction')
        self.assertEqual(transaction.amount, 50.0)
        self.assertEqual(transaction.type, 'Transaction')

    def test_amount_validation(self):
        with self.assertRaises(NoNegativeError):
            Credit.objects.create(
                customer=self.trader,
                description='Negative Credit Transaction',
                amount=-50.0
            )

    def test_credit_transaction(self):
        credit_transaction = Credit.objects.create(
            customer=self.trader,
            description='Credit Transaction',
            amount=100.0
        )
        self.assertEqual(credit_transaction.type, 'Credit')
        self.assertEqual(credit_transaction.creditamount, 100.0)
        
        self.assertEqual(
            str(credit_transaction),
            '[CREDIT TRANSACTION] -- Credit Transaction'
        )
        
        self.assertEqual(credit_transaction.customer.balance, 150.0)
        self.assertEqual(self.trader.balance, 150.0)
        self.assertEqual(credit_transaction.balance, 150.0)


    def test_debit_transaction(self):
        debit_transaction = Debit.objects.create(
            customer=self.trader,
            description='Debit Transaction',
            amount=50.0
        )
        self.assertEqual(debit_transaction.type, 'Debit')
        self.assertEqual(debit_transaction.debitamount, 50)
        
        self.assertEqual(
            str(debit_transaction),
            '[DEBIT TRANSACTION] -- Debit Transaction'
        )
        
        self.assertEqual(debit_transaction.customer.balance, 0)
        self.assertEqual(debit_transaction.balance, 0)
