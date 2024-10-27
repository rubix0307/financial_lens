from dataclasses import dataclass
from .models import Receipt, Product, Section, Currency, ProductCategory
from django.contrib.auth import get_user_model
from django.db import transaction, IntegrityError
from typing import Optional
from datetime import datetime


User = get_user_model()

@dataclass
class ServiceProductData:
    name: str
    name_original: str
    price: float
    category: ProductCategory
    name_en: Optional[str] = None
    name_ru: Optional[str] = None
    name_ua: Optional[str] = None

@dataclass
class ServiceReceiptData:
    shop_name: str
    shop_address: str
    owner: User
    section: Section
    currency: Currency
    date: datetime
    photo: str
    products: list[ServiceProductData] = None


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
                    name_en=product_data.name_en or product_data.name,
                    name_ru=product_data.name_ru or product_data.name,
                    name_ua=product_data.name_ua or product_data.name,
                    price=product_data.price,
                    category=product_data.category,
                    receipt=receipt,
                )
                for product_data in products_data
            ]
            Product.objects.bulk_create(products)
            return products
        except IntegrityError:
            return None

    @staticmethod
    @transaction.atomic
    def create_receipt_with_products(receipt_data: ServiceReceiptData) -> Optional[tuple[Receipt, list[Product]]]:

        receipt = ReceiptService.create_receipt(receipt_data)
        if receipt is None:
            return None

        return receipt, ReceiptService.create_products(receipt, receipt_data.products)
