from django.contrib.auth import get_user_model
from django.test import TestCase
from unittest.mock import Mock
from datetime import datetime

from common.adaptors import ProductDataToServiceAdapter, ReceiptDataToServiceAdapter
from currency.models import Currency
from open_ai.structures import ProductData, ReceiptData
from receipt.models import ProductCategory
from section.models import Section


User = get_user_model()

class ProductDataToServiceAdapterTest(TestCase):
    def setUp(self):
        # Set up mock data for testing
        self.category = ProductCategory.objects.create(name="Test Category")
        self.product_data = ProductData(
            category_id=self.category.id,
            name_original="Test Product",
            name_en="Test Product",
            name_ru="Тестовый продукт",
            price=100.0,
        )

    def test_to_service_product_data(self):
        adapter = ProductDataToServiceAdapter(self.product_data, self.category)
        service_product_data = adapter.to_service_product_data()

        # Test if conversion is correct
        self.assertEqual(service_product_data.name, "Test Product")
        self.assertEqual(service_product_data.name_original, self.product_data.name_original)
        self.assertEqual(service_product_data.price, self.product_data.price)
        self.assertEqual(service_product_data.category, self.category)
        self.assertEqual(service_product_data.name_en, self.product_data.name_en)


class ReceiptDataToServiceAdapterTest(TestCase):
    def setUp(self):
        # Set up mock data for testing
        self.owner = User.objects.create(username="testuser")
        self.section = Section.objects.create(name="Test Section")
        self.currency = Currency.objects.create(code="USD")
        self.photo = "test_photo.jpg"

        self.category1 = ProductCategory.objects.create(name="Test Category 1")
        self.category2 = ProductCategory.objects.create(name="Test Category 2")

        self.product_data_1 = ProductData(
            category_id=self.category1.id,
            name_en="Test Product 1",
            price=50.0,
        )
        self.product_data_2 = ProductData(
            category_id=self.category2.id,
            name_en="Test Product 2",
            price=75.0,
        )

        self.receipt_data = ReceiptData(
            shop_name="Test Shop",
            shop_address="123 Test St",
            products=[self.product_data_1, self.product_data_2],
            currency="USD",
            date="2024-10-26",
        )

    def test_to_service_receipt_data(self):
        adapter = ReceiptDataToServiceAdapter(
            receipt_data=self.receipt_data,
            owner=self.owner,
            section=self.section,
            currency=self.currency,
            photo=self.photo,
        )

        service_receipt_data = adapter.to_service_receipt_data()

        self.assertEqual(service_receipt_data.shop_name, self.receipt_data.shop_name)
        self.assertEqual(service_receipt_data.shop_address, self.receipt_data.shop_address)
        self.assertEqual(service_receipt_data.owner, self.owner)
        self.assertEqual(service_receipt_data.section, self.section)
        self.assertEqual(service_receipt_data.currency, self.currency)
        self.assertEqual(service_receipt_data.photo, self.photo)
        self.assertEqual(service_receipt_data.date, datetime.strptime(self.receipt_data.date, '%Y-%m-%d'))
        self.assertEqual(len(service_receipt_data.products), 2)


        service_product_1 = service_receipt_data.products[0]
        service_product_2 = service_receipt_data.products[1]

        self.assertEqual(service_product_1.name, self.product_data_1.name_en)
        self.assertEqual(service_product_1.price, self.product_data_1.price)
        self.assertEqual(service_product_1.category, self.category1)

        self.assertEqual(service_product_2.name, self.product_data_2.name_en)
        self.assertEqual(service_product_2.price, self.product_data_2.price)
        self.assertEqual(service_product_2.category, self.category2)
