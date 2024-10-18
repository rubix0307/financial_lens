from django.contrib import admin
from .models import CustomUser


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username')
    search_fields = ('username',)

admin.site.register(CustomUser, CustomUserAdmin)
