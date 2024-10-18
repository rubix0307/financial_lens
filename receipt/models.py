from django.contrib.auth import get_user_model
from django.db import models


class Receipt(models.Model):
    shop_name = models.CharField(max_length=255, null=True, blank=True)
    shop_address = models.CharField(max_length=1024, null=True, blank=True)
    photo = models.ImageField(upload_to='receipt/', null=True, blank=True, max_length=1024)
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    date = models.DateTimeField()

    def __str__(self):
        return f'{self.pk}'

    def save(self, *args, **kwargs):
        return super(Receipt, self).save(*args, **kwargs)

    class Meta:
        db_table = 'receipt'


class Product(models.Model):
    name = models.CharField(max_length=255)
    name_original = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=20, decimal_places=2)
    category = models.ForeignKey('ProductCategory', on_delete=models.CASCADE, null=True, blank=True)
    receipt = models.ForeignKey(Receipt, on_delete=models.CASCADE, related_name='products')

    def save(self, *args, **kwargs):
        if not self.name_original:
            self.name_original = self.name

        super(Product, self).save(*args, **kwargs)
        return self

    class Meta:
        db_table = 'receipt_product'
        ordering = ['id']


class ProductCategory(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'receipt_product_category'

