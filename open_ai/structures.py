from dataclasses import dataclass, fields


@dataclass
class Product:
    category_id: int = None
    name_en: str = None
    name_original: str = None
    name_ru: str = None
    name_ua: str = None
    price: float = None

@dataclass
class ReceiptData:
    is_recipe: bool = False
    shop_address: str = None
    shop_name: str = None
    products: list[Product] = None
    currency: str = None
    date: str = None

    def __init__(self, **kwargs):
        valid_fields = {f.name for f in fields(self)}
        for key, value in kwargs.items():
            if key in valid_fields:
                setattr(self, key, value)
