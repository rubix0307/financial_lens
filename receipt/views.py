from django.http import HttpResponseNotFound, JsonResponse
from django.shortcuts import get_object_or_404, render

from .forms import ReceiptForm
from .models import Receipt
from .services import delete_receipt, get_paginated_receipts


def receipt_list_view(request):
    section_id = request.GET.get('section', 1)
    page = request.GET.get('page', 1)
    per_page = request.GET.get('per_page', 3)
    paginated_receipts = get_paginated_receipts(section_id, page, per_page)
    return render(request, 'receipt/feed/receipt_list.html', {'receipts': paginated_receipts})


def receipt_detail_view(request, receipt_id):
    receipt = get_object_or_404(Receipt, id=receipt_id)
    if request.method == 'GET':
        form = ReceiptForm(instance=receipt)
        return render(request, 'receipt/detail/receipt.html', {'form': form, 'receipt': receipt})

    elif request.method == 'POST':
        form = ReceiptForm(request.POST, request.FILES, instance=receipt)
        if form.is_valid():
            form.save()
            return JsonResponse({'message': 'Receipt updated successfully'})
        else:
            return JsonResponse({'errors': form.errors}, status=400)


def receipt_delete_view(request, receipt_id):
    if request.method == 'POST':
        receipt = delete_receipt(receipt_id)
        if receipt:
            return JsonResponse({'message': 'Receipt deleted successfully'})
        else:
            return HttpResponseNotFound('Receipt not found')
    return JsonResponse({'error': 'Invalid request method'}, status=405)

