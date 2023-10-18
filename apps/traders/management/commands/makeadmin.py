# yourapp/management/commands/makeadmin.py
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = 'Seed the database with 10 traders having $100 each'

    def handle(self, *args,  **options):
        # Check if there are already traders in the database.
        
        if User.objects.filter(is_superuser = True).exists():
            self.stdout.write(self.style.WARNING('An admin user already exists in the database'))
            return #super().handle(*args,  **options)
        
        User.objects.create_superuser(email = 'admin@ftnja.com', password = 'admin')
        self.stdout.write(self.style.SUCCESS(f'Successfully created admin: password:admin, email:admin@ftnja.com'))
