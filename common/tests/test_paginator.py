from django.core.paginator import Page
from django.test import TestCase

from common.services.paginator import get_paginated_objects, PaginatedResult


class TestPaginationService(TestCase):

    def setUp(self):
        self.data = [i for i in range(1, 51)]

    def test_first_page(self):
        page_number = 1
        per_page = 10
        result = get_paginated_objects(self.data, page_number, per_page)

        self.assertIsInstance(result, PaginatedResult)
        self.assertEqual(result.current_page, 1)
        self.assertEqual(result.total_pages, 5)
        self.assertEqual(result.total_items, 50)
        self.assertEqual(len(result.items), 10)
        self.assertTrue(result.has_next)
        self.assertFalse(result.has_previous)
        self.assertEqual(result.next_page_number, 2)
        self.assertIsNone(result.previous_page_number)

    def test_middle_page(self):
        page_number = 3
        per_page = 10
        result = get_paginated_objects(self.data, page_number, per_page)

        self.assertIsInstance(result, PaginatedResult)
        self.assertEqual(result.current_page, 3)
        self.assertEqual(result.total_pages, 5)
        self.assertEqual(result.total_items, 50)
        self.assertEqual(len(result.items), 10)
        self.assertTrue(result.has_next)
        self.assertTrue(result.has_previous)
        self.assertEqual(result.next_page_number, 4)
        self.assertEqual(result.previous_page_number, 2)

    def test_last_page(self):
        page_number = 5
        per_page = 10
        result = get_paginated_objects(self.data, page_number, per_page)

        self.assertIsInstance(result, PaginatedResult)
        self.assertEqual(result.current_page, 5)
        self.assertEqual(result.total_pages, 5)
        self.assertEqual(result.total_items, 50)
        self.assertEqual(len(result.items), 10)
        self.assertFalse(result.has_next)
        self.assertTrue(result.has_previous)
        self.assertIsNone(result.next_page_number)
        self.assertEqual(result.previous_page_number, 4)

    def test_page_out_of_range(self):
        page_number = 10
        per_page = 10
        result = get_paginated_objects(self.data, page_number, per_page)

        self.assertIsInstance(result, PaginatedResult)
        self.assertEqual(result.current_page, 5)
        self.assertEqual(result.total_pages, 5)
        self.assertEqual(len(result.items), 10)

    def test_invalid_page_number(self):
        page_number = 'invalid'
        per_page = 10
        result = get_paginated_objects(self.data, page_number, per_page)

        self.assertIsInstance(result, PaginatedResult)
        self.assertEqual(result.current_page, 1)
        self.assertEqual(len(result.items), 10)

    def test_negative_page_number(self):
        page_number = -3
        per_page = 10
        result = get_paginated_objects(self.data, page_number, per_page)

        self.assertIsInstance(result, PaginatedResult)
        self.assertEqual(result.current_page, 1)
        self.assertEqual(len(result.items), 10)

    def test_per_page_greater_than_total(self):
        page_number = 1
        per_page = 100
        result = get_paginated_objects(self.data, page_number, per_page)

        self.assertIsInstance(result, PaginatedResult)
        self.assertEqual(result.current_page, 1)
        self.assertEqual(result.total_pages, 1)
        self.assertEqual(result.total_items, 50)
        self.assertEqual(len(result.items), 50)
        self.assertFalse(result.has_next)
        self.assertFalse(result.has_previous)

    def test_empty_list(self):
        page_number = 1
        per_page = 10
        result = get_paginated_objects([], page_number, per_page)

        self.assertIsInstance(result, PaginatedResult)
        self.assertEqual(result.total_pages, 1)
        self.assertEqual(result.total_items, 0)
        self.assertEqual(len(result.items), 0)
        self.assertFalse(result.has_next)
        self.assertFalse(result.has_previous)

    def test_single_object(self):
        page_number = 1
        per_page = 10
        result = get_paginated_objects([1], page_number, per_page)

        self.assertIsInstance(result, PaginatedResult)
        self.assertEqual(result.current_page, 1)
        self.assertEqual(result.total_pages, 1)
        self.assertEqual(result.total_items, 1)
        self.assertEqual(len(result.items), 1)
        self.assertFalse(result.has_next)
        self.assertFalse(result.has_previous)

    def test_call_returns_page_object(self):
        page_number = 1
        per_page = 10
        result = get_paginated_objects(self.data, page_number, per_page)

        page_object = result()
        self.assertIsInstance(page_object, Page)
        self.assertEqual(page_object.number, 1)
        self.assertEqual(len(page_object.object_list), 10)

    def test_str_page_number(self):
        page_number = '1'
        per_page = 10
        result = get_paginated_objects(self.data, page_number, per_page)

        page_object = result()
        self.assertIsInstance(page_object, Page)
        self.assertEqual(page_object.number, 1)
        self.assertEqual(len(page_object.object_list), 10)
