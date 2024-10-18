# Generated by Django 5.1.2 on 2024-10-18 21:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('currency', '0001_initial'),
        ('receipt', '0001_initial'),
        ('section', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='receipt',
            name='currency',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='currency.currency'),
        ),
        migrations.AddField(
            model_name='receipt',
            name='section',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='receipts', to='section.section'),
        ),
    ]
