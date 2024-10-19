from datetime import datetime
from unittest.mock import patch, MagicMock

import pytz
from django.test import TestCase
from django.utils.timezone import make_aware
from django.db import IntegrityError

from .models import Currency, CurrencyRateHistory
from .services import CurrencyRateService


class CurrencyRateServiceTest(TestCase):
    def setUp(self):
        Currency.objects.create(code='USD')
        Currency.objects.create(code='EUR')

    @patch('requests.get')
    def test_fetch_rates_live(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'quotes': {
                'USDEUR': 0.85
            },
            'timestamp': 1633036800
        }
        mock_get.return_value = mock_response

        data = CurrencyRateService.fetch_rates(base_currency='USD')
        self.assertIsNotNone(data)
        self.assertIn('quotes', data)
        self.assertEqual(data['quotes']['USDEUR'], 0.85)

    @patch('requests.get')
    def test_fetch_rates_historical(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'quotes': {
                'USDEUR': 0.84
            },
            'timestamp': 1632950400
        }
        mock_get.return_value = mock_response

        data = CurrencyRateService.fetch_rates(base_currency='USD', date=datetime(2024, 10, 18).date())
        self.assertIsNotNone(data)
        self.assertIn('quotes', data)
        self.assertEqual(data['quotes']['USDEUR'], 0.84)

    @patch('requests.get')
    def test_fetch_rates_empty_data(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {}
        mock_get.return_value = mock_response

        data = CurrencyRateService.fetch_rates(base_currency='USD')
        self.assertIsNone(data)

    @patch('requests.get')
    def test_fetch_rates_future_date(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "error": {
                "code": 302,
                "info": "You have entered an invalid date. [Required format: date=YYYY-MM-DD]"
            },
            "success": False
        }
        mock_get.return_value = mock_response

        future_date = datetime(2100, 1, 1).date()
        data = CurrencyRateService.fetch_rates(base_currency='USD', date=future_date)

        self.assertIsNone(data)

    def test_convert_timestamp_to_datetime(self):
        timestamp = 1633036800
        expected_datetime = make_aware(datetime.utcfromtimestamp(timestamp), pytz.UTC)
        result = CurrencyRateService._convert_timestamp_to_datetime(timestamp)
        self.assertEqual(result, expected_datetime)

    def test_create_missing_currencies(self):
        existing_currencies = CurrencyRateService._get_existing_currencies()
        target_currency_codes = ['USD', 'EUR', 'GBP']

        CurrencyRateService._create_missing_currencies(existing_currencies, target_currency_codes)

        self.assertTrue(Currency.objects.filter(code='GBP').exists())

    @patch('requests.get')
    def test_save_rates(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'quotes': {
                'USDEUR': 0.85,
                'USDGBP': 0.75
            },
            'timestamp': 1633036800
        }
        mock_get.return_value = mock_response

        CurrencyRateService.save_rates(base_currency='USD')

        self.assertTrue(CurrencyRateHistory.objects.filter(currency__code='EUR', per_usd=0.85).exists())
        self.assertTrue(CurrencyRateHistory.objects.filter(currency__code='GBP', per_usd=0.75).exists())

    @patch('requests.get')
    def test_save_rates_with_integrity_error(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'quotes': {
                'USDEUR': 0.85
            },
            'timestamp': 1633036800
        }
        mock_get.return_value = mock_response

        with patch('currency.models.CurrencyRateHistory.objects.bulk_create', side_effect=IntegrityError):
            CurrencyRateService.save_rates(base_currency='USD')

        # Check new row after IntegrityError
        self.assertTrue(CurrencyRateHistory.objects.filter(currency__code='EUR', per_usd=0.85).exists())
        self.assertTrue(CurrencyRateHistory.objects.filter(currency__code='EUR', per_usd=0.85).exists())


