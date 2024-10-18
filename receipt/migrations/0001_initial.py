# Generated by Django 5.1.2 on 2024-10-18 20:57

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'receipt_product_category',
            },
        ),
        migrations.CreateModel(
            name='Receipt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shop_name', models.CharField(blank=True, max_length=255, null=True)),
                ('shop_address', models.CharField(blank=True, max_length=1024, null=True)),
                ('photo', models.ImageField(blank=True, max_length=1024, null=True, upload_to='receipt/')),
                ('date', models.DateTimeField()),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'receipt',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('name_original', models.CharField(max_length=255)),
                ('price', models.DecimalField(decimal_places=2, max_digits=20)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='receipt.productcategory')),
                ('receipt', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='receipt.receipt')),
            ],
            options={
                'db_table': 'receipt_product',
                'ordering': ['id'],
            },
        ),
    ]
