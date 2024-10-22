from django.core.paginator import Page, EmptyPage, PageNotAnInteger, Paginator
from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class PaginatedResult:
    _paginated_objects: Page = field(repr=False)
    items: List
    total_pages: int
    total_items: int
    current_page: int
    has_previous: bool
    has_next: bool
    previous_page_number: Optional[int] = None
    next_page_number: Optional[int] = None

    def __call__(self) -> Page:
        return self._paginated_objects


def get_paginated_objects(obj: List, page: int, per_page: int = 10) -> PaginatedResult:
    """
    Args:
        obj (List): The list of objects to paginate.
        page (int): The current page number.
        per_page (int): The number of objects on the page.

    Returns:
        PaginatedResult: Object with pagination information.
    """

    if type(page) is str and str(page).isdigit():
        page = int(page)

    if type(page) is not int:
        page = 1
    elif page < 1:
        page = 1

    paginator = Paginator(obj, per_page)
    try:
        paginated_objects = paginator.page(page)
    except PageNotAnInteger:
        paginated_objects = paginator.page(1)
    except EmptyPage:
        paginated_objects = paginator.page(paginator.num_pages)

    return PaginatedResult(
        _paginated_objects=paginated_objects,
        items=list(paginated_objects.object_list),
        total_pages=paginator.num_pages,
        total_items=paginator.count,
        current_page=paginated_objects.number,
        has_previous=paginated_objects.has_previous(),
        has_next=paginated_objects.has_next(),
        previous_page_number=paginated_objects.previous_page_number() if paginated_objects.has_previous() else None,
        next_page_number=paginated_objects.next_page_number() if paginated_objects.has_next() else None,
    )
