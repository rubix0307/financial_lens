from django.contrib.auth import get_user_model

from bot.common import SavedMedia
from common.adaptors import ReceiptDataToServiceAdapter
from currency.models import Currency
from open_ai.services import OpenAIService
from receipt.models import Product, Receipt
from receipt.services import ReceiptService
from section.models import Section


User = get_user_model()

class BotService:

    @staticmethod
    def analyze_and_save_receipt(image: SavedMedia, owner: User, section: Section) -> tuple[Receipt, list[Product]]:
        receipt_data = OpenAIService().analyze_receipt(image_path=image.image_path)
        currency = Currency.objects.get(code=receipt_data.currency)
        service_receipt_data = ReceiptDataToServiceAdapter(
            receipt_data=receipt_data,
            owner=owner,
            section=section,
            currency=currency,
            photo=image.image_name,
        ).to_service_receipt_data()

        receipt, products = ReceiptService.create_receipt_with_products(service_receipt_data)
        return receipt, products

