from django import forms
from receipt.models import Receipt


class ReceiptForm(forms.ModelForm):
    class Meta:
        model = Receipt
        fields = ['shop_name', 'shop_address', 'photo', 'date']
