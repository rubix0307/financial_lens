# Generated by Django 5.1.2 on 2024-10-26 18:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('receipt', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='name_en',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='name_ru',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='name_ua',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='productcategory',
            name='name_en',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='productcategory',
            name='name_ru',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='productcategory',
            name='name_ua',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
