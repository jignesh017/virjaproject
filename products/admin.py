from django.contrib import admin
from .models import Product, ProductImage

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'brand', 'price_display', 'is_active', 'is_featured')
    list_filter = ('category', 'brand', 'is_active', 'is_featured')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductImageInline]
    list_editable = ('is_active', 'is_featured')

    def price_display(self, obj):
        return "N/A" # Price not in model yet, placeholder if needed or remove
    price_display.short_description = "Price"
