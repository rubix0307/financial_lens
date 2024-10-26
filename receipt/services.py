from dataclasses import dataclass
from .models import Receipt, Product, Section, Currency, ProductCategory
from django.contrib.auth import get_user_model
from django.db import transaction, IntegrityError
from typing import Optional
from datetime import datetime


User = get_user_model()

@dataclass
class ServiceReceiptData:
    shop_name: str
    shop_address: str
    owner: User
    section: Section
    currency: Currency
    date: datetime
    photo: str

@dataclass
class ServiceProductData:
    name: str
    name_original: str
    price: float
    category: ProductCategory

class ReceiptService:

    @staticmethod
    @transaction.atomic
    def create_receipt(receipt_data: ServiceReceiptData) -> Optional[Receipt]:
        try:
            return Receipt.objects.create(
                shop_name=receipt_data.shop_name,
                shop_address=receipt_data.shop_address,
                owner=receipt_data.owner,
                section=receipt_data.section,
                currency=receipt_data.currency,
                date=receipt_data.date,
                photo=receipt_data.photo,
            )
        except IntegrityError:
            return None

    @staticmethod
    @transaction.atomic
    def create_products(
            receipt: Receipt,
            products_data: list[ServiceProductData]
    ) -> Optional[list[Product]]:
        try:
            products = [
                Product(
                    name=product_data.name,
                    name_original=product_data.name_original,
                    price=product_data.price,
                    category=product_data.category,
                    receipt=receipt,
                )
                for product_data in products_data
            ]
            return Product.objects.bulk_create(products)
        except IntegrityError:
            return None

    @staticmethod
    @transaction.atomic
    def create_receipt_with_products(
            receipt_data: ServiceReceiptData,
            products_data: Optional[list[ServiceProductData]] = None
    ) -> Optional[tuple[Receipt, list[Product]]]:

        if products_data is None:
            products_data = []

        receipt = ReceiptService.create_receipt(receipt_data)
        if receipt is None:
            return None

        products = ReceiptService.create_products(receipt, products_data)
        if products is None:
            return None

        return receipt, products
