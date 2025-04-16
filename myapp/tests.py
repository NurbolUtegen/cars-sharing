from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from myapp.models import Car, Rental
from datetime import date, timedelta
from unittest.mock import patch, MagicMock

class StripeTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')
        self.car = Car.objects.create(model="BMW", price_per_day=100, available=True)
        self.rental = Rental.objects.create(
            user=self.user,
            car=self.car,
            start_date=date.today(),
            end_date=date.today() + timedelta(days=2),
            total_price=200,
        )

    @patch('myapp.views.stripe.checkout.Session.create')
    def test_checkout_session_creation(self, mock_create_session):
        mock_create_session.return_value = MagicMock(id='fake-session-id')
        url = reverse('create_checkout_session', args=[self.rental.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['id'], 'fake-session-id')


