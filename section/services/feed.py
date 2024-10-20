from receipt import services as r_services


def get_paginated_receipts(section_id, page=1, per_page=10) -> r_services.get_paginated_receipts:
    page_obj = r_services.get_paginated_receipts(section_id, page, per_page)
    page_obj.object_list = page_obj.object_list.prefetch_related('products')
    return page_obj