from datetime import datetime
from django.contrib.auth import get_user_model

from currency.models import Currency
from open_ai.structures import ProductData, ReceiptData
from receipt.models import ProductCategory
from receipt.services import ServiceProductData, ServiceReceiptData
from section.models import Section


User = get_user_model()

class ProductDataToServiceAdapter:
    def __init__(self, product_data: ProductData, category: ProductCategory):
        self.product_data = product_data
        self.category = category

    def to_service_product_data(self) -> ServiceProductData:
        return ServiceProductData(
            name=self.product_data.name_en or self.product_data.name_original,
            name_original=self.product_data.name_original,
            price=self.product_data.price,
            category=self.category,
            name_en=self.product_data.name_en,
            name_ru=self.product_data.name_ru,
            name_ua=self.product_data.name_ua,
        )

class ReceiptDataToServiceAdapter:
    def __init__(self, receipt_data: ReceiptData, owner: User, section: Section, currency: Currency, photo: str):
        self.receipt_data = receipt_data
        self.owner = owner
        self.section = section
        self.currency = currency
        self.photo = photo

    def to_service_receipt_data(self) -> ServiceReceiptData:
        category_ids = [p.category_id for p in self.receipt_data.products if p.category_id]
        categories_dict = {
            category.id: category
            for category in ProductCategory.objects.filter(id__in=category_ids)
        }

        service_products: list[ServiceProductData] = [
            ProductDataToServiceAdapter(
                product, category=categories_dict.get(product.category_id)
            ).to_service_product_data()
            for product in self.receipt_data.products or []
        ]

        return ServiceReceiptData(
            shop_name=self.receipt_data.shop_name,
            shop_address=self.receipt_data.shop_address,
            owner=self.owner,
            section=self.section,
            currency=self.currency,
            date=datetime.strptime(self.receipt_data.date, '%Y-%m-%d'),
            photo=self.photo,
            products=service_products,
        )
