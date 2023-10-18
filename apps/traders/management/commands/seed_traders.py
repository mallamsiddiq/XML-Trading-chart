# yourapp/management/commands/seed_traders.py
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from authapp.models import Trader  # Import your Trader model
from traders.models import Credit

User = get_user_model()

class Command(BaseCommand):
    help = 'Seed the database with 10 traders having $100 each'

    def handle(self, *args, **options):
        # Check if there are already traders in the database.
        if Trader.objects.exists():
            self.stdout.write(self.style.WARNING('Traders already exist. Skipping seed.'))
            return

        # Create 10 traders and add them to the database.
        for idx in range(10):
            email = f'trader{idx + 1}@gmail.com'
            password = 'password'
            
            # Create a User object (for authentication).
            # # Create a Trader object (linking the User to the Trader model).
            trader = Trader.objects.create_user(email = email, password = password)
            
            
            

            Credit.objects.create(
                customer=trader, 
                description = 'First seeding from admin', 
                amount = 100.0
            )
            
            self.stdout.write(self.style.SUCCESS(f'Successfully created trader: {email}'))
