import itertools

import pytz
import requests
from datetime import datetime, date as date_type
from typing import Dict, List, Optional

from django.conf import settings
from django.db import IntegrityError, transaction
from django.utils.timezone import make_aware

from .models import Currency, CurrencyRateHistory


class CurrencyRateService:
    API_URL_HISTORICAL: str = 'https://api.apilayer.com/currency_data/historical'
    API_URL_LIVE: str = 'https://api.apilayer.com/currency_data/live'
    API_KEYS_COUNT: List[str] = len(settings.APILAYER_API_KEYS)
    API_KEYS_ITERATOR = itertools.cycle(settings.APILAYER_API_KEYS)

    @staticmethod
    def _get_headers(api_key: str) -> Dict[str, str]:
        return {"apikey": api_key}

    @staticmethod
    def _make_request(url: str, params: Dict[str, str], api_key: str) -> Optional[Dict]:
        headers = CurrencyRateService._get_headers(api_key)
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            return response.json()
        return None

    @staticmethod
    def fetch_rates(base_currency: str = 'USD', date: Optional[date_type] = None) -> Optional[Dict]:

        if date is None or date == datetime.now().date():
            url = CurrencyRateService.API_URL_LIVE
            params = {'source': base_currency}
        else:
            url = CurrencyRateService.API_URL_HISTORICAL
            params = {
                'source': base_currency,
                'date': date.strftime('%Y-%m-%d')
            }

        for i in range(CurrencyRateService.API_KEYS_COUNT):
            api_key = next(CurrencyRateService.API_KEYS_ITERATOR)
            data = CurrencyRateService._make_request(url, params, api_key)

            if data and data.get('success', True):
                return data
        else:
            # TODO logging
            pass

        return None

    @staticmethod
    def _convert_timestamp_to_datetime(timestamp: Optional[int], timezone=pytz.UTC) -> datetime:
        """
        Converts timestamp to a datetime object, taking into account the time zone.
        """
        if timestamp:
            return make_aware(datetime.utcfromtimestamp(timestamp), timezone=timezone)
        else:
            return make_aware(datetime.now(), timezone=timezone)

    @staticmethod
    def _get_existing_currencies() -> Dict[str, Currency]:
        """
        Loads all currencies from the database and returns them as a dictionary.
        """
        return {currency.code: currency for currency in Currency.objects.all()}

    @staticmethod
    def _create_missing_currencies(existing_currencies: Dict[str, Currency], target_currency_codes: List[str]) -> None:
        """
        Creates new currencies that are not in the database and updates the dictionary of existing currencies.
        """
        new_currency_codes = [code for code in target_currency_codes if code not in existing_currencies]
        new_currencies = [Currency(code=code) for code in new_currency_codes]

        if new_currencies:
            Currency.objects.bulk_create(new_currencies)
            created_currencies = Currency.objects.filter(code__in=new_currency_codes)
            existing_currencies.update({currency.code: currency for currency in created_currencies})

    @staticmethod
    def _prepare_currency_rate_history_objects(
        existing_currencies: Dict[str, Currency], data: Dict, date_obj: datetime
    ) -> List[CurrencyRateHistory]:
        """
        Prepares a list of CurrencyRateHistory objects to be saved.
        """
        currency_rate_history_objects = []
        for pair, rate in data['quotes'].items():
            target_currency_code = pair[3:]
            currency = existing_currencies[target_currency_code]
            currency_rate_history_objects.append(
                CurrencyRateHistory(
                    currency=currency,
                    per_usd=rate,
                    date=date_obj
                )
            )
        return currency_rate_history_objects

    @staticmethod
    def _save_currency_rate_history_objects(currency_rate_history_objects: List[CurrencyRateHistory]) -> None:
        """
        Saves CurrencyRateHistory objects en masse. If it fails, saves one at a time.
        """
        try:
            CurrencyRateHistory.objects.bulk_create(currency_rate_history_objects)
        except IntegrityError:
            for obj in currency_rate_history_objects:
                try:
                    obj.save()
                except IntegrityError:
                    pass  # TODO logging

    @staticmethod
    def save_rates(base_currency: str = 'USD', date: Optional[date_type] = None) -> None:
        """
        The main function of maintaining exchange rates.
        """
        data = CurrencyRateService.fetch_rates(base_currency, date)
        if data and 'quotes' in data:
            date_obj = CurrencyRateService._convert_timestamp_to_datetime(data.get('timestamp'))

            existing_currencies = CurrencyRateService._get_existing_currencies()
            target_currency_codes = [pair[3:] for pair in data['quotes'].keys()]
            CurrencyRateService._create_missing_currencies(existing_currencies, target_currency_codes)

            currency_rate_history_objects = CurrencyRateService._prepare_currency_rate_history_objects(
                existing_currencies, data, date_obj
            )

            with transaction.atomic():
                CurrencyRateService._save_currency_rate_history_objects(currency_rate_history_objects)
