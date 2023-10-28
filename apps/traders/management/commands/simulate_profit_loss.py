import random
from django.core.management.base import BaseCommand
from authapp.models import Trader
from traders.models import Credit, Debit
from django.db import transaction as atomic_transaction
from django.contrib.auth import get_user_model
import time

import threading

User = get_user_model()

def make_transaction(**kwargs):
    if kwargs['amount'] < 0:
        return Debit(**kwargs)
    return Credit(**kwargs)

database_lock = threading.Lock()

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

        def simulate_trade(curr_trader):
            
            for minute in range(1, num_transactions + 1):
                # Generate a random transaction amount within the range [-transaction_amount, transaction_amount]
                rand_amount = random.uniform(-transaction_amount, transaction_amount)

                # Create a new transaction record for this trader
                while True:
                    try:
                        with atomic_transaction.atomic():
                            transaction = make_transaction(customer=curr_trader, 
                                          description = '', 
                                          amount = rand_amount)
                            transaction.description = f"{transaction.__class__.__name__} of {rand_amount} @ {minute} Minute"
                            self.stdout.write(self.style.WARNING(f' {transaction.customer}'))
                            with database_lock:
                                transaction.save()
                            self.stdout.write(self.style.MIGRATE_HEADING(f'{transaction.description}  ----->>>>{transaction.customer.balance}'))
                            
                        break  # If the transaction is successful, break the loop
                    except Exception as e:
                        self.stdout.write(self.style.ERROR(f'Error while saving transaction: {curr_trader}{e}'))
                        time.sleep(5)
                time.sleep(delay)
            self.stdout.write(self.style.SUCCESS(f'Simulated profit/loss for trader {curr_trader}'))

        threads = [threading.Thread(target=simulate_trade, args=(trader,)) for trader in traders ]

        [thrd.start() for thrd in threads]

        [thrd.join() for thrd in threads]