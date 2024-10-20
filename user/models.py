from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    last_name = models.CharField(max_length=256, null=True, blank=True)
    telegram_id = models.PositiveBigIntegerField(null=True, blank=True)
    language_code = models.CharField(max_length=2, null=True, blank=True) # ISO 639-1
    password = models.CharField(max_length=256)

    class Meta:
        db_table = 'user'