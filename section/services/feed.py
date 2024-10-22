from common.services.paginator import get_paginated_objects
from receipt.models import Receipt


def get_paginated_receipts(section_id, page=1, per_page=10) -> get_paginated_objects:
    receipts = (Receipt.objects
                .filter(section_id=section_id)
                .order_by('-date', '-id')
                .prefetch_related('products')
                )

    return get_paginated_objects(receipts, page=page, per_page=per_page)