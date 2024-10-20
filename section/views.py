from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import render

from .services.feed import get_paginated_receipts


def index(request: WSGIRequest) -> HttpResponse:
    context = {
        'page_obj': get_paginated_receipts(section_id=1, page=request.GET.get('page', 1), per_page=8)
    }
    return render(request, 'section/index.html', context=context)

def get_feed(request: WSGIRequest) -> HttpResponse:
    return render(request, 'section/index.html')