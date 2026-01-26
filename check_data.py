import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vproject.settings')
django.setup()

from products.models import Product

slug = 'schneider-electric-mcb-488a'
try:
    product = Product.objects.get(slug=slug)
    print(f"Product: {product.name}")
    print(f"Slug: {product.slug}")
    print(f"Category: {product.category}")
    if product.category:
        print(f"Category Name: {product.category.name}")
        print(f"Category Slug: {product.category.slug}")
except Exception as e:
    print(f"Error: {e}")
