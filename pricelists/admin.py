from django.contrib import admin
from .models import PriceList

@admin.register(PriceList)
class PriceListAdmin(admin.ModelAdmin):
    list_display = ('title', 'brand', 'created_at')
    list_filter = ('brand',)
    search_fields = ('title', 'brand__name')