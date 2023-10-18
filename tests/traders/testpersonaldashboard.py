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

class TraderDasboardViewTest(TestCase):
    
    def setUp(self):
        # Create an admin user
        self.admin_user = User.objects.create_user(email = 'admin',
            password='adminpass'
        )
        self.admin_user.is_staff = True
        self.admin_user.save()

        # Create a trader user
        self.trader = Trader.objects.create_user('trader', password='traderpass')
        self.trader2 = Trader.objects.create_user('trader2', password='trader2pass')

    def test_admin_can_access_dashboard(self):
        self.client.login(email='admin', password='adminpass')
        response = self.client.get(reverse('chart', args=[self.trader2.pk]))
        self.assertEqual(response.status_code, 200)
        self.client.logout()

    def test_trader_cannot_access_other_traders_dashboards(self):
        self.client.login(email='trader', password='traderpass')
        response = self.client.get(reverse('chart', args=[self.trader2.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('dashboard'))

        messages = list(response.wsgi_request._messages)
        self.assertEqual(len(messages), 1)  # Expecting one message

        # Extract and check the message content
        message = messages[0]
        self.assertEqual(str(message), "Only your Dashboard is accesible to you")
