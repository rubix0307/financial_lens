import datetime
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils.timezone import get_current_timezone, make_aware

from common.services.paginator import PaginatedResult
from receipt.models import Receipt, Product
from section.models import Section
from section.services.feed import get_paginated_receipts

class TestReceiptPaginationService(TestCase):


    def setUp(self):
        User = get_user_model()
        owner = User.objects.create_user(id=1, username="testuser", password="password")
        section = Section.objects.create(name="Test Section")
        self.section = section
        tz = get_current_timezone()

        receipts = []
        for i in range(1, 31):
            receipt_date = make_aware(datetime.datetime(2023, 1, i), timezone=tz)
            receipt = Receipt(owner=owner, section=section, date=receipt_date)
            receipts.append(receipt)
        Receipt.objects.bulk_create(receipts)

        products = []
        for i, receipt in enumerate(Receipt.objects.filter(section=section), start=1):
            product = Product(name=f"Product {i}", receipt=receipt, price=1)
            products.append(product)
        Product.objects.bulk_create(products)

        other_section = Section.objects.create(name="Other Section")
        other_receipt_date = make_aware(datetime.datetime(2023, 2, 1), timezone=tz)
        Receipt.objects.create(owner=owner, section=other_section, date=other_receipt_date)

    def test_paginated_receipts_first_page(self):
        page_number = 1
        per_page = 10
        result = get_paginated_receipts(self.section.id, page_number, per_page)

        self.assertIsInstance(result, PaginatedResult)
        self.assertEqual(result.current_page, 1)
        self.assertEqual(result.total_pages, 3)
        self.assertEqual(result.total_items, 30)
        self.assertEqual(len(result.items), 10)
        self.assertTrue(result.has_next)
        self.assertFalse(result.has_previous)
        self.assertEqual(result.next_page_number, 2)
        self.assertIsNone(result.previous_page_number)

    def test_paginated_receipts_empty_section(self):
        empty_section = Section.objects.create(name="Empty Section")
        page_number = 1
        per_page = 10
        result = get_paginated_receipts(empty_section.id, page_number, per_page)

        self.assertIsInstance(result, PaginatedResult)
        self.assertEqual(result.current_page, 1)
        self.assertEqual(result.total_pages, 1)
        self.assertEqual(result.total_items, 0)
        self.assertEqual(len(result.items), 0)
        self.assertFalse(result.has_next)
        self.assertFalse(result.has_previous)

    def test_receipts_filtered_by_section(self):
        other_section = Section.objects.get(name="Other Section")
        page_number = 1
        per_page = 10
        result = get_paginated_receipts(other_section.id, page_number, per_page)

        self.assertIsInstance(result, PaginatedResult)
        self.assertEqual(result.total_items, 1)
        self.assertEqual(result.items[0].section, other_section)
