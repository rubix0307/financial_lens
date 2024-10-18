from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import get_object_or_404
from .models import Receipt


def get_paginated_receipts(page, per_page=10):
    receipts = Receipt.objects.all().order_by('-date', '-id')
    paginator = Paginator(receipts, per_page)
    try:
        paginated_receipts = paginator.page(page)
    except PageNotAnInteger:
        paginated_receipts = paginator.page(1)
    except EmptyPage:
        paginated_receipts = paginator.page(paginator.num_pages)
    return paginated_receipts


def get_receipt(receipt_id, get_404=True):
    if get_404:
        return get_object_or_404(Receipt, id=receipt_id)
    else:
        try:
            return Receipt.objects.get(id=receipt_id)
        except Receipt.DoesNotExist:
            return None


def update_receipt(receipt_id, get_404=False, **kwargs):
    receipt = get_receipt(receipt_id, get_404=get_404)
    if receipt:
        for field, value in kwargs.items():
            setattr(receipt, field, value)
        receipt.save()
    return receipt


def delete_receipt(receipt_id, get_404=False):
    receipt = get_receipt(receipt_id, get_404=get_404)
    if receipt:
        receipt.delete()
    return receipt
