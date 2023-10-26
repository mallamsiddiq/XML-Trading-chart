import random
from django.core.management.base import BaseCommand
from authapp.models import Trader
from traders.models import Credit, Debit
from django.contrib.auth import get_user_model
import time

User = get_user_model()

def make_transaction(**kwargs):
    if kwargs['amount'] < 0:
        return Debit(**kwargs)
    return Credit(**kwargs)

class Command(BaseCommand):
    help = 'Simulate profit and loss for traders'

    def add_arguments(self, parser):
        # Define an optional command-line argument for num_transactions with a default value of 60
        parser.add_argument('--num_transactions', type=int, default=60, help='Number of minutes for the simulation')
        
        # Define an optional command-line argument for delay with a default value of 20 seconds
        parser.add_argument('--delay', type=int, default=20, help='Number of minutes for the simulation')

    def handle(self, *args, **options):
        num_transactions = options['num_transactions']
        delay = options['delay']
        # Initialize Django for database access
        # django.setup()

        # Get all traders from the database
        self.stdout.write(self.style.MIGRATE_HEADING(f'Okay, we are trading'))

        traders = Trader.objects.all()

        transaction_amount = 15  # Maximum transaction amount range for each minute

        for trader in traders:
            for minute in range(1, num_transactions + 1):
                # Generate a random transaction amount within the range [-transaction_amount, transaction_amount]
                transaction_amount = random.uniform(-transaction_amount, transaction_amount)

                # Create a new transaction record for this trader
                transaction = make_transaction(customer=trader, 
                                          description = '', 
                                          amount = transaction_amount)
                transaction.description = f"{transaction.__class__.__name__} of {transaction_amount} @ {minute} Minute"
                self.stdout.write(self.style.ERROR(f' {transaction.customer}'))

                self.stdout.write(self.style.MIGRATE_HEADING(f'{transaction.customer}  ----->>>>ss'))
                transaction.save()
                self.stdout.write(self.style.MIGRATE_HEADING(f'{transaction.description}  ----->>>>{transaction.customer.balance}'))

                time.sleep(delay)
                

            self.stdout.write(self.style.SUCCESS(f'Simulated profit/loss for trader {trader}'))