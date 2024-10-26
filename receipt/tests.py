from django.test import TestCase
from .models import Section, Currency, ProductCategory
from .services import ReceiptService, ServiceReceiptData, ServiceProductData
from django.contrib.auth import get_user_model
from django.utils import timezone


User = get_user_model()

class ReceiptServiceTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.section = Section.objects.create(name='Test Section')
        self.currency = Currency.objects.create(code='USD')
        self.product_category = ProductCategory.objects.create(name='Test Category')
        self.date = timezone.now()

    def test_create_receipt_success(self):
        receipt_data = ServiceReceiptData(
            shop_name='Test Shop',
            shop_address='123 Test St',
            owner=self.user,
            section=self.section,
            currency=self.currency,
            date=self.date,
            photo='test_photo.jpg',
        )
        receipt = ReceiptService.create_receipt(receipt_data)
        self.assertIsNotNone(receipt)
        self.assertEqual(receipt.shop_name, 'Test Shop')
        self.assertEqual(receipt.owner, self.user)

    def test_create_receipt_failure(self):
        receipt_data = ServiceReceiptData(
            shop_name='Test Shop',
            shop_address='123 Test St',
            owner=None,  # Invalid owner
            section=self.section,
            currency=self.currency,
            date=self.date,
            photo='test_photo.jpg',
        )
        receipt = ReceiptService.create_receipt(receipt_data)
        self.assertIsNone(receipt)

    def test_create_products_success(self):
        receipt_data = ServiceReceiptData(
            shop_name='Test Shop',
            shop_address='123 Test St',
            owner=self.user,
            section=self.section,
            currency=self.currency,
            date=self.date,
            photo='test_photo.jpg',
        )
        receipt = ReceiptService.create_receipt(receipt_data)
        products_data = [
            ServiceProductData(
                name='Product 1',
                name_original='Product Original 1',
                price=10.0,
                category=self.product_category,
            ),
            ServiceProductData(
                name='Product 2',
                name_original='Product Original 2',
                price=20.0,
                category=self.product_category,
            )
        ]
        products = ReceiptService.create_products(receipt, products_data)
        self.assertIsNotNone(products)
        self.assertEqual(len(products), 2)
        self.assertEqual(products[0].name, 'Product 1')
        self.assertEqual(products[1].price, 20.0)

    def test_create_products_failure(self):
        receipt_data = ServiceReceiptData(
            shop_name='Test Shop',
            shop_address='123 Test St',
            owner=self.user,
            section=self.section,
            currency=self.currency,
            date=self.date,
            photo='test_photo.jpg',
        )
        receipt = ReceiptService.create_receipt(receipt_data)
        products_data = [
            ServiceProductData(
                name='Product 1',
                name_original='Product Original 1',
                price=None, # Invalid price
                category=self.product_category,
            )
        ]
        products = ReceiptService.create_products(receipt, products_data)
        self.assertIsNone(products)

    def test_create_receipt_with_products_success(self):
        receipt_data = ServiceReceiptData(
            shop_name='Test Shop',
            shop_address='123 Test St',
            owner=self.user,
            section=self.section,
            currency=self.currency,
            date=self.date,
            photo='test_photo.jpg',
        )
        products_data = [
            ServiceProductData(
                name='Product 1',
                name_original='Product Original 1',
                price=10.0,
                category=self.product_category,
            ),
            ServiceProductData(
                name='Product 2',
                name_original='Product Original 2',
                price=20.0,
                category=self.product_category,
            )
        ]
        result = ReceiptService.create_receipt_with_products(receipt_data, products_data)
        self.assertIsNotNone(result)
        receipt, products = result
        self.assertEqual(receipt.shop_name, 'Test Shop')
        self.assertEqual(len(products), 2)

    def test_create_receipt_with_products_failure(self):
        receipt_data = ServiceReceiptData(
            shop_name='Test Shop',
            shop_address='123 Test St',
            owner=None,  # Invalid owner
            section=self.section,
            currency=self.currency,
            date=self.date,
            photo='test_photo.jpg',
        )
        products_data = [
            ServiceProductData(
                name='Product 1',
                name_original='Product Original 1',
                price=10.0,
                category=self.product_category,
            )
        ]
        result = ReceiptService.create_receipt_with_products(receipt_data, products_data)
        self.assertIsNone(result)
